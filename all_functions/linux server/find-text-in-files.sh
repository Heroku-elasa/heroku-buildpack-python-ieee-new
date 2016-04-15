	grep -r 'js/tinymce/jscripts/tiny_mce' $HOME/app-root/runtime/repo/p2/*
grep -r 'sale' $HOME/app-root/runtime/repo/php/p6*
grep -r 'extension=php_xmlrpc.dll' $HOME/app-root/runtime/repo/php/


find  -type f -exec grep -H 'display_errors' {} +