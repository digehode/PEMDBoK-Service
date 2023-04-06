"""
MKDocs macro module with useful functions when creating tutorials
"""
from io import StringIO
import sys
import math
import os
import builtins
import markdown
# import html

def evalCap(code:str, typed=None, colour=False):
    """
    Evaluate given python code, optionally simyulating typed input

    Args:
        code(string): python code to execute
        typed(string or None): None, or a string of characters to pipe into standard input

    Returns:
        string: the output that the executed code sends to stdout
    """
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    old_stdin = sys.stdin

    old_input=builtins.input     #Deal with missing carriage returns and invisible input
    def myinput(prompt):
        data= old_input(prompt)
        displaydata=data
        if colour:
            displaydata=f"<span class='code-input'>{data}</span>"
        print(displaydata)
        return data
    input=myinput

    if typed!=None:
        sys.stdin = StringIO(typed)
    redirected_input = sys.stdin
    exec(code, {"__name__":"__main__"})
    sys.stdout = old_stdout
    sys.stdin = old_stdin
    input=old_input
    return redirected_output.getvalue()





def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """
    # import the predefined macro
    #fix_url = env.variables.fix_url # make relative urls point to root


    # @env.macro
    # def button(label, url):
    #     "Add a button"
    #     url = fix_url(url)
    #     HTML = """<a class='button' href="%s">%s</a>"""
    #     return HTML % (url, label)


    @env.macro
    def todo(message: str):
        """
        Display state span in output
        """
        return(f"<div class='todo'>{markdown.markdown(message)}</div>")


    @env.macro
    def version_info():

        draftStatus="DRAFT"
        if env.variables['extra']['draft']==0:
            draftStatus="RELEASED"
        year=env.variables['extra']['year']
        return f"""
 - **Year:** {year}
 - **Status:** {draftStatus}
"""

    
    @env.macro
    def state(state: str):
        """
        Display state span in output
        """
        
        text=state
        if state.upper()=="A":
            text="TODO "
        elif state.upper()=="B":
            text="REVIEW"
        elif state.upper()=="C":
            text="DONE "
        if env.variables['extra']['draft']!=0:
            return(f" <span class='state state-{state}'>[{text}]</span>")
        else:
            return ""

    
    # @env.macro
    # def state(state: str):
    #     """
    #     Display state span in output
    #     """
    #     return(f"<span class='state-{state}'>{state}</span>")

    
    @env.macro
    def code_from_file(fn: str, start: int = None, stop: int = None, flavor: str = "", download=False, execute=False, typed=None, colour=False):
        """
        Load code from a file and save as a preformatted code block.
        Start and stop can also be used to indicate the starting line and the stopping line
        you wish to extract from the file. 
        If a flavor is specified, it's passed in as a hint for syntax highlighters.

        Example usage in markdown:

            {{ code_from_file("code/myfile.py", flavor = "python") }}
            {{ code_from_file("code/myfile.py", 2, 5) }}
            {{ code_from_file("code/myfile.py", stop = 5) }}
            {{ code_from_file("code/myfile.py", 2, 5, "python") }}
        """
        docs_dir = env.variables.get("./docs_dir", "docs")
        relative_fn = os.path.join(docs_dir, fn)
        full_fn = os.path.abspath(os.path.join(docs_dir, fn))
        if not os.path.exists(relative_fn):
            return f"""<b>File not found: {fn}</b> - relative: {relative_fn}, full: {full_fn}"""
        with open(relative_fn, "r") as f:
            fr=str(start or "the beginning")
            to=str(stop or  "the end")
            btn= "" if not download else button("Download this file",fn)
            btn=f"<span class='dlbtn'>{btn}</span>"

            output=f"<div class='codeblock'><div class='codetitle'><code>{os.path.basename(full_fn)} from {fr} to {to} </code> {btn} </div>\n"

            temp = []
            x = f.readlines()
            
            # a fix to change python slicing to code line numbers, includes the final integer now.
            if start != None and start > 0:
                start = start -1 
            if stop != None:
                stop = stop + 1
            
            for line in x:
                temp.append(line)

            code="".join(temp[start:stop])
            output+=f"""```python \n{code} \n```\n\n"""
            if typed!=None:
                output+="<div class='codetitle'>Given input</div>\n"
                output+=f"""```\n{typed}\n```\n\n"""


            if execute:
                output+="<div class='codetitle'>Output</div>\n"
                output+=f"""\n<div class="highlight"><pre><span></span><code>{evalCap(code, typed=typed, colour=colour)}</code></pre></div>\n\n\n"""

            output+="\n</div>"
            return output

    @env.macro
    def external_markdown(fn: str):
        """
        Load markdown from files external to the mkdocs root path.
        Example usage in markdown:

            {{external_markdown("../../README.md")}}

        """
        docs_dir = env.variables.get("docs_dir", "docs")
        fn = os.path.abspath(os.path.join(docs_dir, fn))
        if not os.path.exists(fn):
            return f"""<b>File not found: {fn}</b>"""
        with open(fn, "r") as f:
            return f.read()
    
    
    
if __name__=="__main__":
    print(evalCap("print('hello inception')"))
    code="""d=input('enter some text: ')
print(f"You entered '{d}'")
"""
    print(evalCap(code, typed="hello"))
    print(evalCap(code, typed="hello", colour=True))
