Name:		doxgen
Version:	0.0.2
Release:	1%{?dist}
License:	GPLv3
Summary:	Document generator
URL:		https://github.com/tieugene/doxgen/
Source0:	https://github.com/tieugene/doxgen/archive/%{name}-%{version}.tar.bz2
BuildRequires:	python3-setuptools
# python3-devel
BuildRequires:	pkgconfig(python3)
# python3-django
Requires:		python3dist(django)
# default hardcoded converters to PDF
# - HTML (python3-weasyprint)
Recommends:	python3dist(weasyprint)
# - RML
Recommends:	python3-tkrml2pdf
# - PDF form (python3-jpype, java-11-openjdk-headless)
Recommends:	python3dist(jpype1) jre-headless
# can be replaced in code
# - HTML
Suggests: python3-pdfkit wkhtmltopf
# - RML
Suggests: python3-z3c.rml

%description
DoxGen - an application to fill out and print template documents.
Template formats: HTML, RML, PDF forms, ODF.
Output: HTML, PDF.


%prep
%autosetup


%build
%py3_build


%install
%py3_install --install-lib=%{_datadir}
# TODO: rm eggs

%check
%py3_build check


%files
%license LICENSE
%doc README.md doc/INSTALL.md
%{_datadir}/%{name}/


%changelog
* Wed Jan 20 2021 TI_Eugene <ti.eugene@gmail.com> - 0.1.0-1
- Initial build
