from xml.dom.minidom import parseString as string_to_dom
import pathlib

tags = ["a", "abbr", "acronym", "address", "area", "b", "base", "bdo", "big", "blockquote", "body", "br", "button",
        "caption", "cite", "code", "col", "colgroup", "dd", "del", "dfn", "div", "dl", "DOCTYPE", "dt", "em",
        "fieldset", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "html", "hr", "i", "img", "input", "ins", "kbd",
        "label", "legend", "li", "link", "map", "meta", "noscript", "object", "ol", "optgroup", "option", "p", "param",
        "pre", "q", "samp", "script", "select", "small", "span", "strong", "style", "sub", "sup", "table", "tbody",
        "td", "textarea", "tfoot", "th", "thead", "title", "tr", "tt", "ul", "var"]


def Attributes(args: dict):
    """
    It takes a dictionary of attributes and returns a string of attributes

    :param args: a dictionary of attributes and their values
    :type args: dict
    :return: A string of attributes
    """
    if args is not None:
        arg_list = []
        for x in args:
            arg_list.append(f' {x.lower()}="{args[x]}"')
        attributes = ""
        for i in arg_list:
            attributes = attributes + i
        return attributes
    else:
        return ""


def Internals(args: tuple):
    """
    It takes a tuple of strings and returns a string of all the strings in the tuple concatenated together

    :param args: tuple
    :type args: tuple
    :return: the internals of the tuple.
    """
    internals = ""
    if args is not None:
        for x in args:
            internals = internals + x
    return internals


def Customtag(tag: str, *args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<{tag}{attributes}>{internals}</{tag}>"


def HTMLStarter(**attributes):
    attributes = Attributes(attributes)
    return f"<!DOCTYPE html{attributes}>"




def Comment(content: str):
    return f"<!--{content}-->"




class Generate:

    def __init__(self, *args):
        """the arguments for the html generator"""
        html = ""
        for x in args:
            html = html + x
        self.html = html

    def prettify(self, html: bool = True):
        """will give back the properly indented and multiline version of the html"""
        dom = string_to_dom(string=str(self.mini()))
        ugly = dom.toprettyxml(indent="  ")
        split = list(filter(lambda x: len(x.strip()), ugly.split('\n')))
        if html:
            split = split[1:]
        pretty = '\n'.join(split)
        return pretty

    def pretty_print(self):
        """Will print the prettified version of the html"""
        print(self.prettify())

    def mini(self):
        """Will give back the minified version of the html"""
        return self.html

    def write(self, filename: pathlib.Path, mini: bool = True):
        """Used to write the html that is generated to a file. If the file path does not exist it will be created"""
        with filename.open("w") as f:
            f.write(self.mini() if mini is True else self.prettify())


def A(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<a{attributes}>{internals}</a>"


def Abbr(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<abbr{attributes}>{internals}</abbr>"


def Acronym(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<acronym{attributes}>{internals}</acronym>"


def Address(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<address{attributes}>{internals}</address>"


def Area(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<area{attributes}>{internals}</area>"


def B(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<b{attributes}>{internals}</b>"


def Base(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<base{attributes}>{internals}</base>"


def Bdo(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<bdo{attributes}>{internals}</bdo>"


def Big(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<big{attributes}>{internals}</big>"


def Blockquote(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<blockquote{attributes}>{internals}</blockquote>"


def Body(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<body{attributes}>{internals}</body>"


def Br(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<br{attributes}>{internals}</br>"


def Button(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<button{attributes}>{internals}</button>"


def Caption(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<caption{attributes}>{internals}</caption>"


def Cite(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<cite{attributes}>{internals}</cite>"


def Code(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<code{attributes}>{internals}</code>"


def Col(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<col{attributes}>{internals}</col>"


def Colgroup(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<colgroup{attributes}>{internals}</colgroup>"


def Dd(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<dd{attributes}>{internals}</dd>"


def Del(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<del{attributes}>{internals}</del>"


def Dfn(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<dfn{attributes}>{internals}</dfn>"


def Div(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<div{attributes}>{internals}</div>"


def Dl(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<dl{attributes}>{internals}</dl>"


def Doctype(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<DOCTYPE{attributes}>{internals}</DOCTYPE>"


def Dt(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<dt{attributes}>{internals}</dt>"


def Em(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<em{attributes}>{internals}</em>"


def Fieldset(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<fieldset{attributes}>{internals}</fieldset>"


def Form(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<form{attributes}>{internals}</form>"


def H1(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<h1{attributes}>{internals}</h1>"


def H2(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<h2{attributes}>{internals}</h2>"


def H3(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<h3{attributes}>{internals}</h3>"


def H4(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<h4{attributes}>{internals}</h4>"


def H5(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<h5{attributes}>{internals}</h5>"


def H6(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<h6{attributes}>{internals}</h6>"


def Head(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<head{attributes}>{internals}</head>"


def Html(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<html{attributes}>{internals}</html>"


def Hr(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<hr{attributes}>{internals}</hr>"


def I(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<i{attributes}>{internals}</i>"


def Img(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<img{attributes}>{internals}</img>"


def Input(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<input{attributes}>{internals}</input>"


def Ins(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<ins{attributes}>{internals}</ins>"


def Kbd(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<kbd{attributes}>{internals}</kbd>"


def Label(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<label{attributes}>{internals}</label>"


def Legend(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<legend{attributes}>{internals}</legend>"


def Li(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<li{attributes}>{internals}</li>"


def Link(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<link{attributes}>{internals}</link>"


def Map(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<map{attributes}>{internals}</map>"


def Meta(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<meta{attributes}>{internals}</meta>"


def Noscript(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<noscript{attributes}>{internals}</noscript>"


def Object(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<object{attributes}>{internals}</object>"


def Ol(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<ol{attributes}>{internals}</ol>"


def Optgroup(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<optgroup{attributes}>{internals}</optgroup>"


def Option(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<option{attributes}>{internals}</option>"


def P(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<p{attributes}>{internals}</p>"


def Param(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<param{attributes}>{internals}</param>"


def Pre(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<pre{attributes}>{internals}</pre>"


def Q(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<q{attributes}>{internals}</q>"


def Samp(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<samp{attributes}>{internals}</samp>"


def Script(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<script{attributes}>{internals}</script>"


def Select(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<select{attributes}>{internals}</select>"


def Small(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<small{attributes}>{internals}</small>"


def Span(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<span{attributes}>{internals}</span>"


def Strong(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<strong{attributes}>{internals}</strong>"


def Style(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<style{attributes}>{internals}</style>"


def Sub(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<sub{attributes}>{internals}</sub>"


def Sup(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<sup{attributes}>{internals}</sup>"


def Table(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<table{attributes}>{internals}</table>"


def Tbody(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<tbody{attributes}>{internals}</tbody>"


def Td(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<td{attributes}>{internals}</td>"


def Textarea(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<textarea{attributes}>{internals}</textarea>"


def Tfoot(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<tfoot{attributes}>{internals}</tfoot>"


def Th(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<th{attributes}>{internals}</th>"


def Thead(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<thead{attributes}>{internals}</thead>"


def Title(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<title{attributes}>{internals}</title>"


def Tr(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<tr{attributes}>{internals}</tr>"


def Tt(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<tt{attributes}>{internals}</tt>"


def Ul(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<ul{attributes}>{internals}</ul>"


def Var(*args, **attributes):
    attributes = Attributes(attributes)
    internals = Internals(args)
    return f"<var{attributes}>{internals}</var>"
