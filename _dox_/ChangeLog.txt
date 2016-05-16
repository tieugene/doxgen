201207xx: 0.0.7:
	* new templates
	* UI:
		* date calendar widget ('widget' attribute)
		* iconified buttons
		* print/preview for registered users
		* added examples
		* removed initial values
		* <fieldset>ed forms
	* Code:
		* special fields: INN, OGRN (w/ validators)
		* tpl: field wrapper (for easy form tpl customization - e.g. w/ <fieldset>)
		* inharitable auto_form.html (semi-auto custom form)
		* Std refs (SSRF, Okved)
		* 21001 - new fields
20120320:
	* consts.py
	* @try_tpl decorator
	* F21001 starting
20120319:
	* model changed: created/updated stay DateTime
	* admin.py improved
	* auto_list as table
	* 'name' removed from Doc.data
	* 'name' field removed from Anon form
	* Cancel button in Anon/Add/Edit
	* NAME, COMMENTS, UUID => DATA
	- consts.py
20120318:
	* doc_u (update)
	* production: tpl path fixed
	* production: staticfiles ok (doxgen.conf)
	* production: admin media ok (static/admin symlink)
	* login/logout redirect ("?next=" in url)
20120317:
	* pre_print: splitting lines
	* doc_l (list)
	* doc_c (add/create)
	* doc_r (read/view/detail)
	* doc_d (delete)
	* doc_p (print)
20120316:
	* admin url ok
	* login/logout ok (but bad redirect)
20120315:
	* <tpl>.ANON
	* doc_a(FORM)
	* doc_a(DynaForm)
	* initial=today()
	* form_auto.html
	* DB (models)
20120314:
	* doc_a (autoanon) starting
	* utils.py
