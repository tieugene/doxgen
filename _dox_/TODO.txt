* сервис проверки:
** inn
** kpp (ssrf(2)+soun?(2)+kpp?(2)+pk(3))
** ogrn
** адреса
* move k-v tables into k-v DBs
* kpp_field
* addr_field (с проверкой по КЛАДР)
* comments - в "?" и/или title
* прилепить http://dox.eap.su в демки
* перейти на другой движок

= z0008 =
+ CourierNew, 18pt
+ Все - заглавными
+ для граждан - лист А=003, лист Б=004
+ в примере "г СПб" - убрать
+ лист Б - фио не заполняется
+ solo: ограничить оквэды - 4 символа
+ solo: д => дом
+ solo: серия документа - с пробелом
+ solo: телефон = "+7(код)номер, без пробелов

= Try =
* svg
* scribus (svg)
* inkscape
* LyX
* tex

= HTML2PDF =
* wkhtmltopdf - ext binary
* http://code.google.com/p/py-webkit-html-manipulator/ - нечто маленькое и странное - но тоже PyQt4
* http://shallowsky.com/blog/programming/html-slides-to-pdf.html - can't pagebreak
* http://code.google.com/p/pywebkitgtk/ - can't pagebreak
* git://github.com/antialize/wkhtmltopdf.git + https://github.com/mreiferson/py-wkhtmltox

= PDF Forms =
* http://code.google.com/p/pyfpdf/ - судя по всему - только рисовать; форм не берет; парсер html2pdf - использует web2py
* poppler

= PDF =
* pyPdf

= OKVED =
ОК 029-2001 (КДЕС ред. 1) - 20030101:
	Изменений 2/2011 (с 20110901):
		+74.60.1	Оценка уязвимости объектов транспортной инфраструктуры и транспортных средств от актов незаконного вмешательства
		+74.60.2	Проведение расследований и обеспечение безопасности, кроме оценки уязвимости объектов транспортной инфраструктуры и транспортных средств от актов незаконного вмешательства
	Изменений 3/2011 (с 20120101):
		+75.23.5	Деятельность Следственного комитета Российской Федерации
		+75.23.51	Деятельность центрального аппарата Следственного комитета Российской Федерации
		+75.23.52	Деятельность Главного военного следственного управления, главных следственных управлений и следственных управлений Следственного комитета Российской Федерации по субъектам Российской Федерации (в том числе подразделений указанных управлений по административным округам) и приравненных к ним специализированных (в том числе военных) следственных управлений и следственных отделов Следственного комитета Российской Федерации
ОК 029-2007 (КДЕС Ред. 1.1) - 20080101
	1/2007:
		1 > 1.1 (тотально)
	2/2011:
		+74.60.1
		+74.60.2
	3/2011:
		+75.23.5
		+75.23.51
		+75.23.52

http://stackoverflow.com/questions/5682694/django-output-form-errors-as-table-rows-in-form-as-table
http://habrahabr.ru/post/95681/

= z0005 =
* remove empty fields

' '.join(list(s))
Django: {{ s|make_list|join:" " }}

====
* z0002 (21001):
	* add okved:
		* 3 modes: handly/with_guide/from_ref; on start: 1 and 3
		* check+add:
			1. find all selected okveds
			2. find last (or 1st empty) input fieldset
			3. add values (id_okved-0-code, id_okved-0-name, add_another())
			4. patch okved-TOTAL_FORMS, okved-INITIAL_FORMS,
			5. add empty fieldset
			6. remove checks
		* ajax

URLS:
	http://dreamhelg.ru/2011/02/css-position-in-10-steps/
	http://softwaremaniacs.org/blog/category/primer/
	http://sbform.ru/
	http://www.sberbank.biz/formtax.html
	http://blanker.ru/album
	http://www.gnivc.ru/inf_provision/form_templates/
