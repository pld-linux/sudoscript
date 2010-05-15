# TODO:
#	- sudoscriptd in /etc/rc.d/init.d
#	- man ss.1 should be gzipped
#	- better place for pm library

Summary:	Sudoscript provides an audited shell with sudo(8) and script(1)
Name:		sudoscript
Version:	2.1.2
Release:	1
License:	Artistic
Group:		Applications/System
Source0:	http://sudoscript.org/%{name}-%{version}.tar.gz
# Source0-md5:	ac0f8128eef9bf19f06092a1a6d6cf94
Patch0:		%{name}-init.patch
Patch1:		%{name}-parallel-make.patch
URL:		http://sudoscript.org
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
Requires:	/sbin/chkconfig
Requires:	perl-base
Requires:	sudo
Provides:	ss
Provides:	sudoscriptd
Provides:	sudoshell
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The sudoscript package provides audited shells using sudo(8) and
script(1) The package consists of two components. One is a daemon,
sudoscriptd. The other is a front-end program called sudoshell, also
aliased to ss. Sudo is used to authenticate and authorize ss to run as
another user. The audit trail is produced with script(1). When it has
successfully run a new process using sudo, ss runs script(1) with a
FIFO (named pipe) maintained by sudoscriptd as the typescript. The
daemon reads the FIFO and manages back-end log files to store the
session audit. It also adds a session ID and timestamp to the data, so
multiple sessions can be seperated in the log. The daemon limits the
size of the logs produced, since they can grow quite large.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} doc

%install
rm -rf $RPM_BUILD_ROOT
%{__make} \
	DESTDIR=$RPM_BUILD_ROOT \
	SSRPM="n" \
	INSTALL=install \
	TAR=tar \
	RM=rm \
	install

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add sudoscriptd
%service sudoscriptd restart

%preun
if [ "$1" = "0" ]; then
	%service sudoscriptd stop
	/sbin/chkconfig --del sudoscriptd
fi

%files
%defattr(644,root,root,755)
%doc README
%doc INSTALL
%doc SECURITY
%doc SUDOCONFIG
%doc PORTING
%doc PROBLEMS
%doc CHANGELOG
%doc RELEASENOTES
%doc PORCMOLSULB.xml
%doc PORCMOLSULB.html
%doc PORCMOLSULB.pdf
%doc sudoscriptd-src.html
%doc sudoshell-src.html
%doc sudoscript.8.html
%doc sudoscriptd.8.html
%doc Sudoscript.3pm.html
%doc sudoshell.1.html
%doc 2.0arch.xml
%doc 2.0arch.html
%doc 2.0arch.gif
%doc xsl/egbokdoc.xsl
%doc xsl/egbokdoc2fop.xsl
%doc dtd/egbokdoc.dtd
%attr(754,root,root) /etc/init.d/sudoscriptd
%attr(755,root,root) %{_bindir}/sudoshell
%attr(700,root,daemon) %{_sbindir}/sudoscriptd
%attr(755,root,root) %{_bindir}/ss
%dir %{_prefix}/lib/sudoscript
%{_prefix}/lib/sudoscript/Sudoscript.pm
%{_mandir}/man1/sudoshell.1*
%{_mandir}/man1/ss.1*
%{_mandir}/man8/sudoscriptd.8*
%{_mandir}/man8/sudoscript.8*
%{_mandir}/man3/Sudoscript.3pm*
