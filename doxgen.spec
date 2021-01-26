Name:		doxgen
Version:	0.1.0
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
