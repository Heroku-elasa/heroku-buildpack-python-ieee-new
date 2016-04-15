<?php

header("content-type: text/xml");
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
?>
<Response sendDigits="31">
<Say voice='man'>Hello Welcome.</Say>

<Gather numDigits="1" method="POST">
<Say>
Press 1 to call again.
Press any other key to start over.
</Say>
</Gather>
</Response> 
