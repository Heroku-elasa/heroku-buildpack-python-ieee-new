
__author__ = 'http://www.cs.virginia.edu/~lab2q/lesson_7/'

# Import the cgi, os, and Cookie modules.
import cgi, os, Cookie

# Define function to set a cookie.
def set_client_Cookie():
    # Create a Cookie object.
    a_cookie = Cookie.SmartCookie()

    # Assign the cookie a value.
    a_cookie["user"] = "Python"

    # Required header that tells the browser how to render the HTML.
    print "Content-Type: text/html"

    # Send the cookie back to the client.
    print a_cookie, "\n\n"

    # Print the cookie value.
    print "<HTML><BODY>"
    print a_cookie["user"].value, "user cookie set.\n"
    print "<FORM METHOD = post ACTION = \"example_7.4.cgi\">\n"
    print "<INPUT TYPE = \"hidden\" NAME = \
    \"set\" VALUE =\"yes\">\n"
    print "<INPUT TYPE = \"submit\" VALUE = \"Go\"></FORM>\n"
    print "</BODY></HTML>\n"

    # Define function to read a cookie.
    def read_client_Cookie():
    # Create a Cookie object.
        a_cookie = Cookie.SmartCookie( os.environ.get("HTTP_COOKIE", "") )

    # Assign the variable a cookie value.
    cookie_val = a_cookie["user"].value

    # Required header that tells the browser how to render the HTML.
    print "Content-Type: text/html\n\n"

    # Print the cookie value.
    print "<HTML><BODY>"
    print cookie_val, "user cookie read from client.\n"
    print "</BODY></HTML>\n"

    # Define main function.
    def main():
        form = cgi.FieldStorage()
    if (form.has_key("set")):
        if (form["set"].value == "yes"):
            read_client_Cookie()
    else:
        set_client_Cookie()

    # Call main function.
    main()