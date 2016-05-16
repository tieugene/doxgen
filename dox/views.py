# -*- coding: utf-8 -*-

# 1. django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context, loader
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic.list_detail import object_list, object_detail
from django.utils.datastructures import SortedDict

# 2. system
import os, imp, json, pprint

# 3. 3rd party

# 4. my
import utils, forms, models, converter
from consts import *

moduledict = dict()

PAGE_SIZE = 20

def	__log_request(request):
	'''
	.method == .META['REQUEST_METHOD']
	.encoding == None
	.path_info == .META['PATH_INFO']
	'''
	#pprint.pprint(request.META)
	if not settings.DEBUG:
	#if True:
		# 1. sanitize
		meta = request.META
		for k in meta.keys():
			if k.islower():
				del(meta[k])
		# 2. save
		#models.Log(data=json.dumps(meta, indent=1, ensure_ascii=False)).save()
		models.Log(
			method=(request.META['REQUEST_METHOD']=='GET'),
			ip=request.META['REMOTE_ADDR'],
			path=request.META['PATH_INFO'][:254],
			agent=request.META.get('HTTP_USER_AGENT', 'noname')[:254],
			data=json.dumps(meta, indent=1, ensure_ascii=False)
		).save()

def	__load_modules(path):
	'''
	Load all Python modules from a directory into a dict.

	:param path: the path to the living place of the modules to load.
	:type path: :class:`str`
	:returns: map between loaded modules name and their content.
	:rtype: :class:`dict`
	'''
	dir_list = os.listdir(path)
	mods = {}
	for fname in dir_list:
		name, ext = os.path.splitext(fname)
		if ext == '.py' and not name == '__init__':
			f, filename, descr = imp.find_module(name, [path])
			mods[name] = imp.load_module(name, f, filename, descr)
	return mods

def	__try_tpl():
	global moduledict	#, modulelist
	if (not moduledict):
		# 1. load modules into list of modulename=>module
		tpl = __load_modules(os.path.join(os.path.dirname(__file__), 'tpl'))	# {'z0000': <module>}
		# 2. repack
		for k, module in tpl.iteritems():	# k: filename, v: module object
			# try: dict, getattr/setattr/hasattr/delattr, hash/hex/id
			s = set(dir(module))
			data = module.DATA
			uuid = data[K_T_UUID]
			__tryget = module.__dict__.get
			# 2. dict
			moduledict[uuid] = { K_V_MODULE: module, }
			# 3. add dates fields
			datefields = list()
			for i, j in data[K_T_FIELD].iteritems():	# each field definition:
				if (j[K_T_FIELD_T] == K_DATE_FIELD):
					datefields.append(i)
			if (datefields):
				moduledict[uuid][K_V_DATES] = set(datefields)
			# 4. form
			if (K_T_FORM in module.__dict__):		# create DynaForm
				form = module[K_T_FORM]
			else:
				form = forms.GenForm(fieldlist= data[K_T_FIELD])
			moduledict[uuid][K_T_FORM] = form
			# 5. formsets
			if (K_T_FORMSETS in module.__dict__):		# create DynaForm
				formsets = module[K_T_FORMSETS]
			else:
				if (K_T_S in data):
					formsets = forms.GenFormSets(formlist=data[K_T_S])
				else:
					formsets = SortedDict()
			moduledict[uuid][K_T_FORMSETS] = formsets

def	__try_to_call(t, f, v):
	'''
	Try to call function f of module t[] with value v
	'''
	if (f in t[K_V_MODULE].__dict__):
		return t[K_V_MODULE].__dict__[f](v)

def	try_tpl(fn):
	def _wrapped(*args, **kwargs):
		__try_tpl()
		return fn(*args, **kwargs)
	return _wrapped

@try_tpl
def	index(request):
	'''
	List of templates
	'''
	__log_request(request)
	return render_to_response('tpl_list.html', context_instance=RequestContext(request, {'data': moduledict,}))

def	log_l(request):
	'''
	Log list
	'''
	return  object_list (
		request,
		queryset = models.Log.objects.order_by('-pk'),
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = 'log_list.html',
	)

def	log_d(request, id):
	'''
	Log detail
	item = models.Log.objects.get(pk=long(id))
	return render_to_response(
		'log_detail.html',
		context_instance=RequestContext(request, {'data': {
			'id': item.pk,
			'date': item.date,
			'meta': item.unpack()
		},})
	)
	'''
	return  object_detail (
		request,
		queryset = models.Log.objects.all(),
		object_id = id,
		template_name = 'log_detail.html',
	)

@try_tpl
def	doc_l(request, uuid):
	'''
	List of documents
	'''
	__log_request(request)
	tpl = moduledict[uuid]
	if request.user.is_authenticated():
		queryset = models.Doc.objects.filter(user=request.user, type=uuid).order_by('name')
	else:
		queryset = models.Doc.objects.none()
	return  object_list (
		request,
		queryset = queryset,
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = tpl[K_V_MODULE].DATA[K_T_T][K_T_T_LIST] if ((K_T_T in tpl[K_V_MODULE].DATA) and (K_T_T_LIST in tpl[K_V_MODULE].DATA[K_T_T])) else 'auto_list.html',
		extra_context = {
			'object': tpl,
		}
	)

def	__doc_print(request, context_dict, template):
		ext = template.rsplit('.', 1)[1]
		return converter.x2pdf[ext](request, context_dict, template)

def	__doc_acu(request, id, mode):
	'''
	Anon/Create/Update
	:param id:int - uuid (anon/create) or doc id (update)
	:param mode:int (0: anon (print), 1: create, 2: update)
	'''
	__log_request(request)
	if (mode == 2):
		item = models.Doc.objects.get(pk=id)	# Update only
		uuid = item.type
		if (uuid not in moduledict):
			return 'Template not found'
	else:
		uuid = id
	if (request.method == 'POST') and (mode > 0) and (request.POST.get('_action', None) in set(('print', 'view'))):
		mode = 0
	tpl = moduledict[uuid]
	# 1. check <pkg>.ANON/CREATE/UPDATE
	self_func = [K_T_F_ANON, K_T_F_ADD, K_T_F_EDIT][mode]
	if (self_func in tpl[K_V_MODULE].__dict__):
		return tpl[K_V_MODULE].__dict__[self_func](request, id)
	# else:
	# 2. get FORM and FORMSETS
	formclass = tpl[K_T_FORM]
	formsetsclass = tpl[K_T_FORMSETS]	# SortedDict of dicts
	if request.method == 'POST':
		#pprint.pprint(request.POST['_action'])
		form = formclass(request.POST)
		if (mode == 0):	# ANON, Create/Update -> view/print
			del form.fields[K_T_F_NAME]
		formlist = SortedDict()
		isvalid = form.is_valid()
		for k, formset in formsetsclass.iteritems():
			formlist[k] = formset(request.POST, prefix=k)
			isvalid = isvalid and formlist[k].is_valid()
		if isvalid:
			data = form.cleaned_data
			# inject formsets into data
			for k, v in formlist.iteritems():
				dataset = list()
				for i in v.cleaned_data:	# list of dicts
					if i:			# reject empty dicts
						dataset.append(i)
				if dataset:			# reject empty lists
					data[k] = dataset	# inject datasets into data
			__try_to_call(tpl, K_T_F_POST_FORM, data)
			# split
			if (mode == 0):		# ANON > PRINT, C/U -> V/P
				if ((K_T_T in tpl[K_V_MODULE].DATA) and (K_T_T_PRINT in tpl[K_V_MODULE].DATA[K_T_T])):
					context_dict = {'data': data}
					template = tpl[K_V_MODULE].DATA[K_T_T][K_T_T_PRINT]
					if (request.POST.get('_action', None) == u'view'):
						__try_to_call(tpl, K_T_F_PRE_VIEW, data)	# Create/Update -> View
						return converter.html2html(request, context_dict, template)
					else:			# Anon/Create/Update -> PRINT
						__try_to_call(tpl, K_T_F_PRE_PRINT, data)
						return __doc_print(request, context_dict, template)
				else:	# tmp dummy
					return redirect('dox.views.index')
			else:	# CREATE/UPDATE -> SAVE
				if (mode == 1):	# CREATE
					name = data[K_T_F_NAME]
				else:
					item.name = data[K_T_F_NAME]
				del data[K_T_F_NAME]
				# convert dates
				if (K_V_DATES in tpl):
					for k in tpl[K_V_DATES]:
						utils.date2str(data, k)
				__try_to_call(tpl, K_T_F_PRE_SAVE, data)
				if (mode == 1):	# CREATE
					# user, type, name, data
					item = models.Doc(user=request.user, type=uuid, name=name, data=json.dumps(data, indent=1, ensure_ascii=False))
				else:
					item.data = json.dumps(data, indent=1, ensure_ascii=False)
				item.save()
				return redirect(doc_r, id=item.pk)
	else:	# GET
		if (mode < 2):		# ANON, CREATE
			form = formclass()
			if (mode == 0):	# ANON
				del form.fields[K_T_F_NAME]
			formlist = SortedDict()
			for k, formset in formsetsclass.iteritems():
				formlist[k] = formset(prefix=k)
		else:			# UPDATE
			data = json.loads(item.data)
			data[K_T_F_NAME] = item.name				# inject name
			# restore dates after loading
			if (K_V_DATES in tpl):
				for k in tpl[K_V_DATES]:
					utils.str2date(data, k)
			#pprint.pprint(data)
			__try_to_call(tpl, K_T_F_POST_LOAD, data)
			#pprint.pprint(data)
			__try_to_call(tpl, K_T_F_PRE_FORM, data)
			# split form and formsets
			# 1. eject formsets
			formlist = SortedDict([])
			for pfx, formset in formsetsclass.iteritems():		# formsetsclass == SortedDict {name: FormSetClass}
				formset_data = dict()
				for i, l in enumerate(data.get(pfx, list())):	# l:str - formset name; l:
					for k, v in l.iteritems():
						formset_data[pfx+'-'+str(i)+'-'+k] = v
				formset_data.update({
					pfx+'-TOTAL_FORMS': len(data[pfx]) if pfx in data else 1,
					pfx+'-INITIAL_FORMS': u'0',
					pfx+'-MAX_NUM_FORMS': u'',
				})
				formlist[pfx] = formset(formset_data, prefix=pfx)
				if (pfx in data):
					del data[pfx]
			# 2. else
			form = formclass(data)
	return render_to_response(
		tpl[K_V_MODULE].DATA[K_T_T][K_T_T_FORM] if ((K_T_T in tpl[K_V_MODULE].DATA) and (K_T_T_FORM in tpl[K_V_MODULE].DATA[K_T_T])) else 'auto_form.html',
		context_instance=RequestContext(request, {
			'name': tpl[K_V_MODULE].DATA[K_T_NAME],
			'comments': tpl[K_V_MODULE].DATA[K_T_COMMENTS],
			'legend': tpl[K_V_MODULE].DATA.get(K_T_LEGEND, ''),
			'uuid': tpl[K_V_MODULE].DATA[K_T_UUID],
			'form': form,
			'formlist': formlist,
			'example': tpl[K_V_MODULE].DATA.get('example', None),
		}))

def	__doc_rvp(request, id, mode):
	'''
	Read/View/Print
	:param mode:enum - mode (0: read, 1: html, 2: pdf)
	'''
	__log_request(request)
	#print "__doc_rvp"
	item = models.Doc.objects.get(pk=id)
	uuid = item.type
	if (uuid not in moduledict):
		return 'Template not found'
	# else:
	tpl = moduledict[uuid]
	self_func = [K_T_F_READ, K_T_F_VIEW, K_T_F_PRINT][mode]
	if (self_func in tpl[K_V_MODULE].__dict__):
		return tpl[K_V_MODULE].__dict__[self_func](request, id)		# ???
	# else:
	data = json.loads(item.data)
	# auto date conversion
	if (K_V_DATES in tpl):
		for k in tpl[K_V_DATES]:
			utils.str2date(data, k)
	__try_to_call(tpl, K_T_F_POST_LOAD, data)
	# split 1: create data dict
	template_key = [K_T_T_READ, K_T_T_VIEW, K_T_T_PRINT][mode]
	if ((K_T_T in tpl[K_V_MODULE].DATA) and (template_key in tpl[K_V_MODULE].DATA[K_T_T])):
		template = tpl[K_V_MODULE].DATA[K_T_T][template_key]
		context_dict = { 'data': data }
	else:						# auto_*
		#print "auto"
		template = ['auto_read.html', 'auto_view.html', 'auto_print.html'][mode]
		# transform data:
		# 1. single values: { key: value, } => [{ k: key, v: value, l: label, h: help }, ]
		datalist = list()
		for k, v in tpl[K_V_MODULE].DATA[K_T_FIELD].iteritems():
			datalist.append({
				'k': k,
				'v': data[k],
				'l': v[K_T_FIELD_A]['label'],
				'h': v[K_T_FIELD_A].get('help_text', None),
			})
		# 2. multivalues: { key: [{k: value,},],} => [{l: label, h: help, t: header, v: [[{value,],],]
		datasets = list()
		if (K_T_S in tpl[K_V_MODULE].DATA):
			for k, v in tpl[K_V_MODULE].DATA[K_T_S].iteritems():
				header = list()
				for i, j in v[K_T_FIELD_T].iteritems():
					header.append(j[K_T_FIELD_A]['label'])
				dataset = list()	# all lines
				if k in data:		# skip empty multivalues
					for rec in data[k]:	# one line in data - dict
						dataset.append(rec.values())
				datasets.append({
					't': header,
					'v': dataset,
					'l': v[K_T_FIELD_A]['label'],
					'h': v[K_T_FIELD_A].get('help_text', None),
				})
		context_dict = {
				'pk':		item.pk,
				'name':		item.name,
				'type':		tpl,
				'datalist':	datalist,
				'datasets':	datasets,
			}
	# split 2: call render
	if (mode < 2):		# READ, VIEW
		__try_to_call(tpl, (K_T_F_PRE_READ, K_T_F_PRE_VIEW)[mode], data)
		#return render_to_response(template, context_instance=RequestContext(request, context_dict))
		return converter.html2html(request, context_dict, template)
	else:			# PRINT
		__try_to_call(tpl, K_T_F_PRE_PRINT, data)
		return __doc_print(request, context_dict, template)

@try_tpl
def	doc_a(request, uuid):
	'''
	Anonymous form
	'''
	return __doc_acu(request, uuid, 0)

@login_required
@try_tpl
def	doc_c(request, uuid):
	'''
	Create document
	'''
	return __doc_acu(request, uuid, 1)

@login_required
@try_tpl
def	doc_u(request, id):
	'''
	Update (edit) document
	'''
	return __doc_acu(request, id, 2)

@login_required
@try_tpl
def	doc_r(request, id):
	'''
	Read (view) document
	'''
	return __doc_rvp(request, id, 0)

@login_required
@try_tpl
def	doc_v(request, id):
	'''
	Preview document
	'''
	return __doc_rvp(request, id, 1)

@login_required
@try_tpl
def	doc_p(request, id):
	'''
	Print document
	'''
	return __doc_rvp(request, id, 2)

@login_required
@try_tpl
def	doc_d(request, id):
	'''
	Delete document
	'''
	item = models.Doc.objects.get(pk=id)
	uuid = item.type
	item.delete()
	if (uuid in moduledict):
		return redirect('dox.views.doc_l', uuid)
	else:
		return redirect('dox.views.index')
