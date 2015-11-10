"""
### Markdown-Python-Graphviz

This module is an extention to [Python-Markdown][pymd] which makes it
possible to embed [Graphviz][gv] syntax into Markdown documents.

### Requirements

Using this module requires:
   * Python-Markdown
   * Graphviz (particularly ``dot``)

### Syntax

Wrap Graphviz definitions within a dot/neato/dotty/lefty tag.

An example document:

    This is some text above a graph.

    <dot>
    digraph a {
        nodesep=1.0;
        rankdir=LR;
        a -> b -> c ->d;
    }
    </dot>

    Some other text between two graphs.

    <neato>
    some graph in neato...
    </neato>

    This is also some text below a graph.

Note that the opening and closing tags should come at the beginning of
their lines and should be immediately followed by a newline.
    
### Usage

    import markdown
    md = markdown.Markdown(
            extensions=['graphviz'], 
            extension_configs={'graphviz' : {'DOT','/usr/bin/dot'}}
    )
    return md.convert(some_text)


[pymd]: http://www.freewisdom.org/projects/python-markdown/ "Python-Markdown"
[gv]: http://www.graphviz.org/ "Graphviz"

"""
import markdown, re, markdown.preprocessors, subprocess

class GraphvizExtension(markdown.Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'FORMAT': ['png', "Default format for generated files"],
            'BINARY_PATH': ['', "Location of dot binary on OS"],
            'WRITE_IMGS_DIR': ['', "OS directory for generating images"],
            'BASE_IMG_LINK_DIR': ['', "Directory for http linking images"]
        }
        
        if len(args):
            for key, value in args[0]:
                self.setConfig(key, value)

        # Override defaults with user settings
        # This is not legacy code but is used instead of the super call below because we have to support the legacy version
        if hasattr(self, 'setConfigs'):
           self.setConfigs(kwargs)    

    def reset(self):
        pass

    def extendMarkdown(self, md, md_globals):
        config = self.getConfigs();
        
        "Add GraphvizExtension to the Markdown instance."
        md.registerExtension(self)
        self.parser = md.parser
        md.preprocessors.add('graphviz', GraphvizPreprocessor(self, md, config), '_begin')

class GraphvizPreprocessor(markdown.preprocessors.Preprocessor):
    "Find all graphviz blocks, generate images and inject image link to generated images."

    def __init__ (self, graphviz, md, config):
        self.graphviz = graphviz
        self.formatters = ["dot", "neato", "lefty", "dotty"]
        
        self.config = config
        
    def run(self, lines):
        start_tags = [ "<%s>" % x for x in self.formatters ]
        end_tags = [ "</%s>" % x for x in self.formatters ]
        graph_n = 0
        new_lines = []
        block = []
        in_block = None
        for line in lines:
            if line in start_tags:
                assert(block == [])
                in_block = self.extract_format(line)
            elif line in end_tags:
                new_lines.append(self.graph(graph_n, in_block, block))
                graph_n = graph_n + 1
                block = []
                in_block = None
            elif in_block in self.formatters:
                block.append(line)
            else:
                new_lines.append(line)
        assert(block == [])
        return new_lines

    def extract_format(self, tag):
        format = tag[1:-1]
        assert(format in self.formatters)
        return format

    def graph(self, n, type, lines):
        "Generates a graph from lines and returns a string containing n image link to created graph."
        assert(type in self.formatters)        
        cmd = "%s%s -T%s" % (self.config['BINARY_PATH'],
                             type,
                             self.config['FORMAT'])
        #print("DEBUG: dot command: ", cmd)
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        #(child_stdin, child_stdout) = (p.stdin, p.stdout)
        #print("DEBUG: lines: ", "\n".join(lines)) 
        p.stdin.write("\n".join(lines).encode('utf-8'))
        p.stdin.close()
        p.wait()
        # if format = SVG then it will be a embedded picture
        if self.config['FORMAT'] == 'svg':
            # this should be a full SVG format
            svg_string = p.stdout.read().decode('utf-8')
            #print("DEBUG: svg:\n ", svg_string)
            # we have to remove the xml header itself and only keep the <svg> tag
            lines = svg_string.splitlines(True)
            outputstring = ''
            startoutput = False
            for line in lines:
                if '<svg' in line:
                    startoutput = True
                if startoutput:
                    outputstring += line
            
            #print("DEBUG: outputstring: \n", outputstring) 
            

            return outputstring
        else:
            filepath = "%s%s.%s" % (self.config['WRITE_IMGS_DIR'], n, self.config['FORMAT'])
            fout = open(filepath, 'bw')
            fout.write(p.stdout.read())
            fout.close()
            output_path = "%s%s.%s" % (self.config['BASE_IMG_LINK_DIR'], n, self.config['FORMAT'])
            return "![Graphviz chart %s](%s)" % (n, output_path)

def makeExtension(*args, **kwargs) :
    return GraphvizExtension(*args, **kwargs)