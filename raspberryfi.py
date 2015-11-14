from HTMLParser import HTMLParser
from libmproxy.models import decoded


injected = ''' 
<script>
    alert("Fuck you.");
</script>
'''


def response(context, flow):
    with decoded(flow.response):
        lineno, line_offset = find_injection_offset(flow.response.content) 
        if lineno is not None and line_offset is not None:
            flow.response.content = inject(flow.response.content, injected,
                lineno, line_offset)


def debug(s):
    with open('out.txt', 'a') as file:
        file.write(str(s) + '\n')


def inject(string, injected, lineno, line_offset):
    true_offset = find_true_offset(string, lineno, line_offset)
    return string[:true_offset] + injected + string[true_offset:]


def find_true_offset(string, lineno, line_offset):
    if lineno > 1:
        newline_count = 1
        for i, c in enumerate(string):
            if c == '\n':
                newline_count += 1
                if newline_count == lineno:
                    return i + line_offset + 1
        raise ValueError('Not enough lines in string.')

    return line_offset 


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
            self.invoke_tag_callback()

    def invoke_tag_callback(self):
        lineno, offset = self.getpos()
        offset += len(self.get_starttag_text())
        self.callback(lineno, offset)
        

class Empty:
    pass
