Summary: Utilities for alternative packaging
Name: scl-utils
Version: 20130529
Release: 17%{?dist}
License: GPLv2+
Group: Applications/File
URL: https://fedorahosted.org/released/scl-utils/
Source0: https://fedorahosted.org/released/scl-utils/%{name}-%{version}.tar.gz
Source1: macros.scl-filesystem
Source2: scl_source
Patch0: 0001-Rename-attr-macros-so-they-are-correctly-named.patch
Patch1: 0002-Implement-as-a-command-separator.patch
Patch2: 0003-Mention-environment-modifying-commands-in-the-man-pa.patch
Patch3: 0004-Check-whether-a-file-was-created-when-doing-mkstemp-.patch
Patch4: 0005-Various-fixes-in-Provides-and-Requires-of-scl-packag.patch
Patch5: 0006-Modified-the-behavior-of-debuginfo-generation-proces.patch
Patch6: 0007-Changed-command-description-in-scl-man-pages.patch
Patch7: 0008-Changed-script-paths-in-__os_install_post.patch
Patch8: 0009-Remove-sclbuild-as-it-s-not-that-useful.patch
Patch9: 0010-Added-capability-to-register-and-deregister-collecti.patch
Patch10: 0011-Fix-missing-allocation-check-in-read_script_output.patch
Patch11: 0012-Introduce-scl_dependency_generators-macro.patch
Patch12: 0013-Add-capability-to-share-collections-using-nfs.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Run-time utility for alternative packaging.

%package build
Summary: RPM build macros for alternative packaging
Group: Applications/File
Requires: iso-codes
Requires: redhat-rpm-config

%description build
Essential RPM build macros for alternative packaging.

%prep
%setup -q
%patch0 -p1 -b .attr-names
%patch1 -p1 -b .command-separator
%patch2 -p1 -b .env-variables-man
%patch3 -p1 -b .coverity-mkstemp
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"

%install
rm -rf %buildroot
mkdir -p %buildroot%{_sysconfdir}/rpm
mkdir -p %buildroot%{_sysconfdir}/scl/prefixes
pushd %buildroot%{_sysconfdir}/scl
ln -s prefixes conf
popd
mkdir -p %buildroot/opt/rh
install -d -m 755 %buildroot%{_mandir}/man1
make install DESTDIR=%buildroot
cat %SOURCE1 >> %buildroot%{_sysconfdir}/rpm/macros.scl
install -m 755 %SOURCE2 %buildroot%{_bindir}/scl_source

# remove brp-python-hardlink invocation as it is not present in RHEL5
%if 0%{?rhel} == 5
  sed -i -e '/^.*brp-python-hardlink.*/d' %buildroot%{_sysconfdir}/rpm/macros.scl
%endif

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,-)
%dir /opt/rh
%{_sysconfdir}/scl/conf
%dir %{_sysconfdir}/scl/prefixes
%{_bindir}/scl
%{_bindir}/scl_enabled
%{_bindir}/scl_source
%{_mandir}/man1/*
%{_sysconfdir}/bash_completion.d/scl.bash

%{!?_rpmconfigdir:%global _rpmconfigdir /usr/lib/rpm}
%files build
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.scl
%{_rpmconfigdir}/scldeps.sh
%{_rpmconfigdir}/fileattrs/scl.attr
%{_rpmconfigdir}/brp-scl-compress
%{_rpmconfigdir}/brp-scl-python-bytecompile

%changelog
* Thu Mar 08 2015 Lubos Karddos <lkardos@redhat.com> - 20130529-17
- Remove /uucp/ from directory structure.

* Thu Mar 05 2015 Lubos Karddos <lkardos@redhat.com> - 20130529-16
- Remove /scls/ from macros  _sysconfdir, _sharedstatedir and _localstatedir

* Tue Jan 27 2015 Lubos Karddos <lkardos@redhat.com> - 20130529-15
- fixed wrong syntax of or-operator in scl.attr

* Tue Jan 06 2015 Jan Zeleny <jzeleny@redhat.com> - 20142529-14
- remove the vendor prefix from %%scl_install

* Tue Jan 06 2015 Jan Zeleny <jzeleny@redhat.com> - 20130529-13
- bump the version to get in sync with 7.1 branch
- Reflect the state of %%nfsmountable macro in collections' rpm macro files
- escape all the %% chars in changelog

* Mon Jan 05 2015 Jan Zeleny <jzeleny@redhat.com> - 20132529-13
- after a thorough discussion with scl maintainers, revert the vendor prefix
  in package names

* Fri Dec 12 2014 Jan Zeleny <jzeleny@redhat.com> - 20132529-12
- the second half of the macro rename

* Fri Dec 12 2014 Jan Zeleny <jzeleny@redhat.com> - 20130529-11
- renamed %%scl_pkg_prefix to %%scl_full_prefix (#1167042)

* Fri Dec 05 2014 Lubos Kardos <lkardos@redhat.com> - 20130529-10
- Allow to use vendor prefix in packages names
- Include %%nfsmountable macro into scl's rpm macros file

* Wed Oct 23 2014 Lubos Kardos <lkardos@redhat.com - 20130529-9
- "filesystem" is now symlink to file "filelist"

* Wed Oct 08 2014 Lubos Kardos <lkardos@redhat.com - 20130529-8
- Modified paths of state and conf files
- Add owning and creating of state and conf files if nfsmountable is defined
- Add printing file names in error messages

* Tue Sep 30 2014 Lubos Kardos <lkardos@redhat.com - 20130529-7
Support for importing collections from NFS mounts
- Add execution of register and deregister scripts during registration
  and deregistration if they exist.
- Add capability to make collection nfs mountable using macro nfsmountable.

* Tue Aug 26 2014 Jan Zeleny <jzeleny@redhat.com> - 20130529-6
Catch up with Fedora and RHEL6
- add automatic Provides: scl-package(%%scl) to all scl packages
  (except for metapackages)
- add automatic Requires: %%scl_runtime to all scl packages
  (except for metapackages)
- the "filesystem" file renamed back to "filelist"
- add correct dependencies to debug packages.
- allow disabling debuginfo generation
- remove automatic creation of debuginfo for metapackage.
- rephrase command description in man page
- fix system paths in __os_install_post
- remove the sclbuild utility, as it's mostly useless
- add the command set to register/deregister collection
- fix missing allocation check in read_script_output()
- drop recursive ownership of /usr/lib within SCL root
- introduce %%scl_dependency_generators macro

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 20130529-5
- Mass rebuild 2014-01-24

* Tue Jan 14 2014 Jan Zeleny <jzeleny@redhat.com> - 20130529-4
- fixed some coverity-reported bugs (related: #1032616)
- a note about env. variables in man page (#968954)
- drop the /var/spool/uucp from the default fs structure (#1033674)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 20130529-3
- Mass rebuild 2013-12-27

* Thu Nov 21 2013 Jan Zeleny <jzeleny@redhat.com> - 20130529-2
- add scl_source script for intercollection dependencies (#1032444)
- updated macros in macros.scl-filesystem (#1032451, #1032451)
- add delimiter between collections and command (#1032460)
- fix the name of attr macros (#1023628)

* Wed May 29 2013 Jan Zeleny <jzeleny@redhat.com> - 20130529-1
- changed the upstream tarball location
- update to 20130529

* Fri Feb 01 2013 Jindrich Novy <jnovy@redhat.com> 20121110-2
- add build compatibility fixes

* Wed Dec 19 2012 Jindrich Novy <jnovy@redhat.com> 20121110-1
- introduce sclbuild utility
- fix exporting of env. variables when mutiple collections are
  enabled at the same time
- better bash completion
- fix changelog

* Thu Sep 27 2012 Jindrich Novy <jnovy@redhat.com> 20120927-1
- update to 20120927
- better BUILDROOT processing
- bash completition for scl command
- debuginfo package now has SCL-specific provide
- non-SCL builds are without warning in build log
- improved help

* Thu Aug 09 2012 Jindrich Novy <jnovy@redhat.com> 20120809-1
- update to 20120809
- processes the SCL buildroot correctly now

* Thu Aug 02 2012 Jindrich Novy <jnovy@redhat.com> 20120802-1
- update to 20120802

* Tue Jul 31 2012 Jindrich Novy <jnovy@redhat.com> 20120731-1
- add functionality that allows to list all packages in a collection
- add dependency generators

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120613-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Jindrich Novy <jnovy@redhat.com> 20120613-1
- Requires: iso-codes for basic filesystem in build subpackage
- add scl_require_package() macro to depend on a particular package
  from the collection
- fix filesystem file list
- tighten runtime package dependency via scl_require()
- fix _localstatedir to point to the correct path according to redhat-rpm-config
- thanks to Bohuslav Kabrda for feature proposals/QA/fixes

* Thu May 03 2012 Jindrich Novy <jnovy@redhat.com> 20120503-1
- avoid doublefree corruption when reading commands from stdin

* Sun Apr 22 2012 Jindrich Novy <jnovy@redhat.com> 20120423-1
- keep filesystem macros out of the main sources as
  it is distro-dependent

* Fri Apr 13 2012 Jindrich Novy <jnovy@redhat.com> 20120413-1
- filesystem ownership by meta package
- add man page
- fix memory leak when parsing commands from stdin
- use more descriptive error message if /etc/prefixes is missing

* Wed Feb 29 2012 Jindrich Novy <jnovy@redhat.com> 20120229-1
- do not prepend scl_* prefix to package names
- unify package naming to <SCL>-package-version
- add scl --list functionality to list available SCLs

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

* Wed Sep 21 2011 Jindrich Novy <jnovy@redhat.com> 0.1-14
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
