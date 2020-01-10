Summary:	Utilities for alternative packaging
Name:		scl-utils
Version:	20120927
Release:	23%{?dist}
License:	GPLv2+
Group:		Applications/File
URL:		http://jnovy.fedorapeople.org/scl-utils/
Source0:	http://jnovy.fedorapeople.org/scl-utils/%{name}-%{version}.tar.gz
Source1:	macros.scl-filesystem
Source2:	scl_source
Patch0: 	0001-Add-all-the-collections-enabled-to-SCLS-env-variable.patch
Patch1: 	0002-Allow-overriding-values-in-scl_package.patch
Patch2: 	0003-Delete-unnecessary-argument-from-check_asprintf.patch
Patch3: 	0004-scl-utils-free.patch
Patch4: 	0005-Use-direct-path-when-calling-scl_enabled.patch
Patch5: 	0006-Execute-enable-scriptlets-only-if-they-are-not-alrea.patch
Patch6: 	0007-Implement-as-a-command-separator.patch
Patch7:     0008-Changed-debuginfo-package-handling.patch
Patch8:     0009-Mention-environment-modifying-commands-in-the-man-pa.patch
Patch9:     0010-Changed-command-description-in-scl-man-pages.patch
Patch10:    0011-Added-capability-to-register-and-deregister-collecti.patch
Patch11:    0012-Fixed-dereferencing-of-null-pointer.patch
Patch12:    0013-Fixed_main_metapackage_dependencies.patch
Patch13:    0014-Add-capability-to-share-collections-using-nfs.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Run-time utility for alternative packaging.

%package build
Summary:	RPM build macros for alternative packaging
Group:		Applications/File
Requires:	iso-codes
Requires:	redhat-rpm-config

%description build
Essential RPM build macros for alternative packaging.

%prep
%setup -q
%patch0 -p1 -b .all-collections
%patch1 -p1 -b .overriding
%patch2 -p1 -b .check-asprintf
%patch3 -p1
%patch4 -p1 -b .direct-path
%patch5 -p1 -b .enable-once
%patch6 -p1 -b .command-separator
%patch7 -p1 -b .debuginfo
%patch8 -p1 -b .man-env
%patch9 -p1 -b .man-command
%patch10 -p1 -b .register
%patch11 -p1 -b .deref
%patch12 -p1 -b .meta-deps
%patch13 -p1 -b .nfsmoutable

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"

%install
rm -rf %buildroot
mkdir -p %buildroot%{_sysconfdir}/rpm
mkdir -p %buildroot%{_sysconfdir}/scl/prefixes
mkdir -p %buildroot/opt/rh
mkdir -p %buildroot%{_rpmconfigdir}/redhat
install -d -m 755 %buildroot%{_mandir}/man1
make install DESTDIR=%buildroot
cat %SOURCE1 >> %buildroot%{_sysconfdir}/rpm/macros.scl
install -m 755 %SOURCE2 %buildroot%{_bindir}/scl_source

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,-)
%dir /opt/rh
%dir %{_sysconfdir}/scl/prefixes
%{_bindir}/scl
%{_bindir}/scl_enabled
%{_bindir}/scl_source
%{_mandir}/man1/*
%{_sysconfdir}/bash_completion.d/scl.bash

%files build
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.scl
%{_rpmconfigdir}/scldeps.sh
%{_rpmconfigdir}/fileattrs/scl.attr
%{_rpmconfigdir}/brp-scl-compress
%{_rpmconfigdir}/brp-scl-python-bytecompile

%changelog
* Wed Oct 08 2014 Lubos Kardos <lkardos@redhat.com - 20120927-23
- Modified paths of state and conf files
- Add owning and creating of state and conf files if nfsmountable is defined
- Add printing file names in error messages

* Thu Sep 25 2014 Jan Zeleny <jzeleny@redhat.com> - 20120927-22
- Add execution of register and deregister scripts during registration
  and deregistration if they exist.
- Add capability to make collection nfs mountable using macro nfsmountable.
- removed the dependency generators and all related changes
  (maintainers' demands)

* Tue Aug 26 2014 Jan Zeleny <jzeleny@redhat.com> - 20120927-21
- fix an obscure segfault when listing collections on i386
- fix registration to work with slash-ended paths
- add the %%scl_dependency_generators macro
- drop recursive ownership of /usr/lib within SCL root

* Fri Aug 01 2014 Jan Zeleny <jzeleny@redhat.com> - 20120927-20
- register and deregister: if there is an error registering or deregistering
  one or more collection, skip it but return non-zero return code
- fix the problem with metapackage dependencies when BuildArch is specified

* Thu Jul 17 2014 Jan Zeleny <jzeleny@redhat.com> - 20120927-19
- register and deregister: include bash completion and help

* Wed Jun 25 2014 Albert Uchytil <auchytil@redhat.com> 20120827-18
- Collection's meta package should now have correct dependencies.

* Mon Jun 23 2014 Albert Uchytil <auchytil@redhat.com> 20120827-17
- Minor changes to prevent possible leaks.

* Fri Jun 20 2014 Albert Uchytil <auchytil@redhat.com> 20120827-16
- fixed dereferencing of a null pointer

* Fri Jun 20 2014 Albert Uchytil <auchytil@redhat.com> 20120827-15
- bumped up release

* Tue Jun 17 2014 Albert Uchytil <auchytil@redhat.com> 20120827-14
- updated man pages
- changed debuginfo package handling (#1113685)
- capability to dynamically register and deregister collections (#1113686)

* Tue Apr 22 2014 Albert Uchytil <auchytil@redhat.com> 20120827-13
- fixed typo in macros.scl

* Mon Apr 14 2014 Albert Uchytil <auchytil@redhat.com> 20120827-12
- new dependency generators for RHEL6 (#1075066, #1075067)

* Fri Mar 28 2014 Jan Zeleny <jzeleny@redhat.com> - 20120827-11
- reverted the last patch, as it breaks some collections. The revert
  is necessary for RHSCL compose, we are looking for other solutions.

* Wed Mar 12 2014 Jan Zeleny <jzeleny@redhat.com> - 20120927-10
- new dependency generators for RHEL6 (#1075067, #1075066)

* Mon Dec 03 2013 Jan Zeleny <jzeleny@redhat.com> - 20120927-8
- back to the original versioning

* Wed Nov 20 2013 Jan Zeleny <jzeleny@redhat.com> - 20120927-8.1
- add scl_source script for intercollection dependencies (#874417)
- updated macros in macros.scl-filesystem (#1029515, #1029516)
- add delimiter between collections and command (#1029517)

* Fri May 17 2013 Jan Zeleny <jzeleny@redhat.com> - 20120927-8
- run enable scriptlet only if the collection is not enabled (#964058)

* Mon Apr 29 2013 Jan Zeleny <jzeleny@redhat.com> - 20120927-7
- use absolute path when calling scl_enabled

* Mon Apr 29 2013 Jan Zeleny <jzeleny@redhat.com> - 20120927-6
- rename scl-utils-free.patch to match the patch naming scheme

* Mon Apr 29 2013 Jan Zeleny <jzeleny@redhat.com> - 20120927-5
- Allow overriding values in macro scl_package (#957185)
- Delete redundant argument from check_asprintf (#957183)
- Enable all collections given as arguments, not just the first one (#949995)
- Prevent collections to be enabled multiple times (#955669)

* Mon Apr 29 2013 Jan Zeleny <jzeleny@redhat.com> - 20120927-4
- prepare for sync with RHEL5 version

* Mon Apr 29 2013 Jan Zeleny <jzeleny@redhat.com> - 20120927-3
- revert the umask patch, as per #953462 and #957702

* Mon Nov 12 2012 Jindrich Novy <jnovy@redhat.com> 20120927-2
- fix usage of freed variable and umask for temp files (#874628)

* Fri Oct 12 2012 Jindrich Novy <jnovy@redhat.com> 20120927-1
- update to 20120927 (#855999)

* Thu Oct  4 2012 Jindrich Novy <jnovy@redhat.com> 20120613-2
- backport patch from upstream to correctly process buildroot
  after installation (compress man pages, etc.) (#844028)

* Fri Jun 22 2012 Jindrich Novy <jnovy@redhat.com> 20120613-1
- update to 20120613 (#855999)

* Thu May 10 2012 Jindrich Novy <jnovy@redhat.com> 20120423-2
- avoid doublefree corruption when reading commands from stdin

* Mon Apr 23 2012 Jindrich Novy <jnovy@redhat.com> 20120423-1
- update to the latest upstream scl-utils-20120423 (#713147)
 - filesystem ownership by meta package
 - add man page
 - fix memory leak when parsing commands from stdin
 - use more descriptive error message if /etc/prefixes is missing
 - do not prepend scl_* prefix to package names
 - unify package naming to <SCL>-package-version
 - add scl --list functionality to list available SCLs

* Wed Feb 15 2012 Jindrich Novy <jnovy@redhat.com> 20120209-2
- build for 6.3

* Thu Feb 09 2012 Jindrich Novy <jnovy@redhat.com> 20120209-1
- fix minor bugs (#788194)
  - clear temp files
  - handle commands from stdin properly
  - run command even if ran as "scl enable SCL command" from already
    enabled SCL

* Wed Jan 25 2012 Jindrich Novy <jnovy@redhat.com> 20120125-1
- remove dsc macros
- trigger scl-utils-build BR inclusion while using scl macros

* Wed Jan 11 2012 Jindrich Novy <jnovy@redhat.com> 20120111-1
- add "dsc" alias to "scl" utility

* Wed Dec 14 2011 Jindrich Novy <jnovy@redhat.com> 20111214-1
- initial review fixes (#767556)

* Fri Dec  9 2011 Jindrich Novy <jnovy@redhat.com> 20111209-1
- allow to use dsc_* macros and dsc* package naming

* Wed Nov 16 2011 Jindrich Novy <jnovy@redhat.com> 20111116-1
- package is now named scl-utils

* Mon Oct 17 2011 Jindrich Novy <jnovy@redhat.com> 20111017-1
- initial packaging for upstream

* Thu Sep 21 2011 Jindrich Novy <jnovy@redhat.com> 0.1-14
- define %%_defaultdocdir to properly relocate docs into
  a stack
- document a way how to pass command to stack via stdin

* Wed Jun 22 2011 Jindrich Novy <jnovy@redhat.com> 0.1-13
- fix Stack meta config configuration

* Fri Jun 17 2011 Jindrich Novy <jnovy@redhat.com> 0.1-12
- use own Stack path configuration mechanism

* Fri Jun 17 2011 Jindrich Novy <jnovy@redhat.com> 0.1-11
- avoid redefinition of %%_root* macros by multiple
  occurence of %%stack_package
- make the Stack root path configurable

* Tue Jun 14 2011 Jindrich Novy <jnovy@redhat.com> 0.1-10
- stack utility allows to read command from stdin

* Mon Jun 13 2011 Jindrich Novy <jnovy@redhat.com> 0.1-9
- introduce stack enablement tracking
- introduce "stack_enabled" helper utility to let a stack
  application figure out which stacks are actually enabled
- disallow running stacks recursively

* Mon Jun 13 2011 Jindrich Novy <jnovy@redhat.com> 0.1-8
- stack utility returns executed commands' exit value

* Fri Jun 10 2011 Jindrich Novy <jnovy@redhat.com> 0.1-7
- fix possible segfault in the stack utility

* Fri Jun 10 2011 Jindrich Novy <jnovy@redhat.com> 0.1-6
- %%stack_name: initial part of stack prefix and name of
  meta package providing scriptlets
- %%stack_prefix: stack namespacing part to be prepended to
  original non-stack package name, can be used for Provides
  namespacing as well
- %%stack_runtime: run-time package name providing scriptlets
- %%stack_require: macro to define dependency to other stacks

* Thu Jun 09 2011 Jindrich Novy <jnovy@redhat.com> 0.1-5
- split the package into two - runtime and build part
- decrease verbosity when enabling a stack

* Wed Jun 08 2011 Jindrich Novy <jnovy@redhat.com> 0.1-4
- prepend stack package with stack_* to prevent namespace
  conflicts with core packages

* Thu Jun 02 2011 Jindrich Novy <jnovy@redhat.com> 0.1-3
- introduce metapackage concept

* Wed Jun 01 2011 Jindrich Novy <jnovy@redhat.com> 0.1-2
- modify macros so that they don't change preamble tags

* Sun May 08 2011 Jindrich Novy <jnovy@redhat.com> 0.1-1
- initial packaging
