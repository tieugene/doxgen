Name:		doxgen
Version:	0.2.0
Release:	1%{?dist}
License:	GPLv3
Summary:	Document generator
URL:		https://github.com/tieugene/doxgen/
Source0:	https://github.com/tieugene/doxgen/archive/%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python3-setuptools
# python3-devel
BuildRequires:	pkgconfig(python3)
# python3-django
Requires:	%{py3_dist django} >= 3.0
# default hardcoded converters to PDF
# - HTML (python3-weasyprint)
Recommends:	%{py3_dist weasyprint}
Suggests: %{py3_dist pdfkit} wkhtmltopf
# - RML
Recommends:	%{py3_dist tkrml2pdf}
Suggests: %{py3_dist z3c.rml}
# - PDF form
Recommends:	%{py3_dist PyPDFForm}

%description
DoxGen - an application to fill out and print template documents.
Template formats: HTML, RML, PDF forms, ODF.
Output: HTML, PDF.


%prep
%autosetup


%build
%py3_build


%install
%py3_install
# py_install not undestands `--install-lib #{_datadir}`
mkdir -p %{buildroot}%{_datadir}
mv %{buildroot}%{python3_sitelib}/%{name} %{buildroot}%{_datadir}/
%{find_lang} django


#check
#py3_build test


%files -f django.lang
%license LICENSE
%doc README.md doc/{INSTALL.md,Plugins.md,doxgen.conf,local_settings.py}
%{_datadir}/%{name}/


%changelog
* Mon Jun 30 2025 TI_Eugene <ti.eugene@gmail.com> - 0.2.0-1
- iText => PyPDFForm
- HTML preview removed

* Sat Jan 30 2021 TI_Eugene <ti.eugene@gmail.com> - 0.1.0-1
- Initial build
