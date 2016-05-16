= Description =
Application to maintain reglament documents.
Output format - PDF[, HTML]
Input formats: HTML, ODF, RML, PDF (form)

= Structures =

== Inner ==

=== now ===

{ field_name: field_value (natural python type), }

=== will ===

...

== DB ==

Doc:
	name:str
	data:json=>dict	# w/o 'name'; dicts can be nested (1 level)

== form ==
{
	'form': forms.Form
	'formsets': SortedDict(formset:FormSet)[]
}
== out ==

(read/print/preview) - similar to inner/Doc
{
	'data': { field_label: field_value, },
}
Note: read - call own tag? Or Doc method?
====
PDF forms:
	* pdftk <file.pdf> generate_fdf output test.fdf - get field names into test.fdf

====
Dependencies:
= Common =
* django-treebeard (http://download.opensuse.org/repositories/home:/TI_Eugene:/python/) - OKVED model
* [*-pymorphy]
* [python-pytils]
= HTML =
** python-wkhtmltopdf (same) (html2pdf)
** wkhtmltopdf (=> xorg-x11-server-Xvfb) (http://code.google.com/p/wkhtmltopdf/) - (html2pdf)
= ODF =
** <s>django-webodt, unoconv</s>
** libreoffice-headless
= RML =
** python-rml2pdf
= PDF =
** xfdftool (=>jre) (http://download.opensuse.org/repositories/home:/TI_Eugene/) (pdf2pdf)

== Howto ==
=== PDF ===
* Ставим Adobe Acrobat Pro 7.0
* Если исходный документ:
-- Word: Create form from - Word
-- не Word - создаем PDF из ёкселя, записываем, Create form from - PDF
* Создаем PDF из файла MSO (Указав Compatibility: Acrobat 7.0 (PDF 1.6))
* В каждом поле - Object - Binding - Name: как будет называться поле
* Save as - Static или Dynamic индифферентно
