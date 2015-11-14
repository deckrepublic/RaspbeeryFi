from HTMLParser import HTMLParser


def debug(s):
    with open('out.txt', 'a') as file:
        file.write(str(s) + '\n')
        

def url_params_to_dict(params_string):
    stuff = dict()

    params = params_string.split('&')
    for param in params:
        split = param.split('=')
        name = split[0]
        value = split[1]
        stuff[name] = value

    return stuff


def inject(string, injected, offset):
    return string[:offset] + injected + string[offset:]


def find_injection_offset(html):
    thing = Empty()

    def callback(lineno, line_offset):
        thing.lineno = lineno
        thing.line_offset = line_offset

    parser = OurHTMLParser()
    parser.callback = callback
    parser.feed(html)

    if thing.lineno is not None and thing.line_offset is not None:
        return find_true_offset(html, thing.lineno, thing.line_offset)
    else:
        return None


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
