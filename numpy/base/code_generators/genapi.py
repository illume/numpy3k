import sys, os, re
import md5

API_FILES = ['arraymethods.c',
             'arrayobject.c',
             'arraytypes.inc.src',
             'multiarraymodule.c',
             'scalartypes.inc.src',
             'ufuncobject.c',
            ]
THIS_DIR = os.path.dirname(__file__)
API_FILES = [os.path.join(THIS_DIR, '..', 'src', a) for a in API_FILES]

def remove_whitespace(s):
    return ''.join(s.split())

class Function(object):
    def __init__(self, name, return_type, args, doc=''):
        self.name = name
        self.return_type = return_type
        self.args = args
        self.doc = doc

    def _format_arg(self, (typename, name)):
        if typename.endswith('*'):
            return typename + name
        else:
            return typename + ' ' + name

    def argtypes_string(self):
        if not self.args:
            return 'void'
        argstr = ', '.join([a[0] for a in self.args])
        return argstr

    def __str__(self):
        argstr = ', '.join([self._format_arg(a) for a in self.args])
        if self.doc:
            doccomment = '/* %s */\n' % self.doc
        else:
            doccomment = ''
        return '%s%s %s(%s)' % (doccomment, self.return_type, self.name, argstr)

    def api_hash(self):
        m = md5.new()
        m.update(remove_whitespace(self.return_type))
        m.update('\000')
        m.update(self.name)
        m.update('\000')
        for typename, name in self.args:
            m.update(remove_whitespace(typename))
            m.update('\000')
        return m.hexdigest()[:8]

class ParseError(Exception):
    def __init__(self, filename, lineno, msg):
        self.filename = filename
        self.lineno = lineno
        self.msg = msg

    def __str__(self):
        return '%s:%s:%s' % (self.filename, self.lineno, self.msg)

def skip_brackets(s, lbrac, rbrac):
    count = 0
    for i, c in enumerate(s):
        if c == lbrac:
            count += 1
        elif c == rbrac:
            count -= 1
        if count == 0:
            return i
    raise ValueError("no match '%s' for '%s' (%r)" % (lbrac, rbrac, s))

def split_arguments(argstr):
    arguments = []
    bracket_counts = {'(': 0, '[': 0}
    current_argument = []
    state = 0
    i = 0
    def finish_arg():
        if current_argument:
            argstr = ''.join(current_argument).strip()
            m = re.match(r'(.*(\s+|[*]))(\w+)$', argstr)
            if m:
                typename = m.group(1).strip()
                name = m.group(3)
            else:
                typename = argstr
                name = ''
            arguments.append((typename, name))
            del current_argument[:]
    while i < len(argstr):
        c = argstr[i]
        if c == ',':
            finish_arg()
        elif c == '(':
            p = skip_brackets(argstr[i:], '(', ')')
            current_argument += argstr[i:i+p]
            i += p-1
        else:
            current_argument += c
        i += 1
    finish_arg()
    return arguments


def find_functions(filename, tag='API'):
    fo = open(filename, 'r')
    functions = []
    return_type = None
    function_name = None
    function_args = []
    doclist = []
    SCANNING, STATE_DOC, STATE_RETTYPE, STATE_NAME, STATE_ARGS = range(5)
    state = SCANNING
    tagcomment = '/*' + tag
    for lineno, line in enumerate(fo):
        try:
            line = line.strip()
            if state == SCANNING:
                if line.startswith(tagcomment):
                    if line.endswith('*/'):
                        state = STATE_RETTYPE
                    else:
                        state = STATE_DOC
            elif state == STATE_DOC:
                if line.startswith('*/'):
                    state = STATE_RETTYPE
                else:
                    line = line.lstrip(' *')
                    doclist.append(line)
            elif state == STATE_RETTYPE: #first line of declaration with return type
                m = re.match(r'static\s+(.*)$', line)
                if m:
                    line = m.group(1)
                return_type = line
                state = STATE_NAME
            elif state == STATE_NAME: # second line, with function name
                m = re.match(r'(\w+)\s*\(', line)
                if m:
                    function_name = m.group(1)
                else:
                    raise ParseError(filename, lineno+1, 'could not find function name')
                function_args.append(line[m.end():])
                state = STATE_ARGS
            elif state == STATE_ARGS:
                if line.startswith('{'): # finished
                    fargs_str = ' '.join(function_args).rstrip(' )')
                    fargs = split_arguments(fargs_str)
                    f = Function(function_name, return_type, fargs,
                                 ' '.join(doclist))
                    functions.append(f)
                    return_type = None
                    function_name = None
                    function_args = []
                    doclist = []
                    state = 0
                else:
                    function_args.append(line)
        except:
            print filename, lineno+1
            raise
    fo.close()
    return functions

def read_order(order_file):
    fo = open(order_file, 'r')
    order = {}
    i = 0
    for line in fo:
        line = line.strip()
        if not line.startswith('#'):
            order[line] = i
            i += 1
    fo.close()
    return order

def get_api_functions(tagname, order_file):
    if not os.path.exists(order_file):
        order_file = os.path.join(THIS_DIR, order_file)
    order = read_order(order_file)
    functions = []
    for f in API_FILES:
        functions.extend(find_functions(f, tagname))
    dfunctions = []
    for func in functions:
        o = order[func.name]
        dfunctions.append( (o, func) )
    dfunctions.sort()
    return [a[1] for a in dfunctions]

def add_api_list(offset, APIname, api_list,
                 module_list, extension_list, init_list):
    """Add the API function declerations to the appropiate lists for use in
    the headers.
    """
    for k, func in enumerate(api_list):
        num = offset + k
        astr = "static %s %s \\\n       (%s);" % \
               (func.return_type, func.name, func.argtypes_string())
        module_list.append(astr)
        astr = "#define %s \\\n        (*(%s (*)(%s)) \\\n"\
               "         %s[%d])" % (func.name,func.return_type,
                                     func.argtypes_string(), APIname, num)
        extension_list.append(astr)
        astr = "        (void *) %s," % func.name
        init_list.append(astr)


def main():
    tagname = sys.argv[1]
    order_file = sys.argv[2]
    functions = get_api_functions(tagname, order_file)
    m = md5.new(tagname)
    for func in functions:
        print func
        ah = func.api_hash()
        m.update(ah)
        print hex(int(ah,16))
    print hex(int(m.hexdigest()[:8],16))

if __name__ == '__main__':
    main()
