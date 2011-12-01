%global mpr_version 3.24-2059-1223-20100508
Summary: Russian man pages from the Linux Documentation Project
Name: man-pages-ru
Version: 0.97
Release: 9%{?dist}
# Source1 has GFDL license
License: BSD and GPL+ and MIT and GFDL
Group: Documentation
URL: http://linuxshare.ru/projects/trans/
# this is rhel only tarball
Source: manpages-ru-%{version}.rh.tar.bz2
Source1: http://downloads.sourceforge.net/%{name}/%{name}_%{mpr_version}.tar.bz2 
# old download sites are not working now
# http://alexm.here.ru/manpages-ru/download/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch


%description
Manual pages from the Linux Documentation Project, translated into
Russian.

%prep
%setup -q -n manpages-ru-%{version}.rh -a 1
# remove bogus pages from Source1:
rm man-pages-ru_%{mpr_version}/man2/gethostid.2
rm man-pages-ru_%{mpr_version}/man2/sethostid.2
rm man-pages-ru_%{mpr_version}/man5/ipc.5

# move Source1 to ./ directory
for i in $(ls man-pages-ru_%{mpr_version});
do
  if [ -d $i ]
  then
    mv man-pages-ru_%{mpr_version}/$i/* $i
  else
    mv man-pages-ru_%{mpr_version}/$i ./
  fi
done
rmdir man-pages-ru_%{mpr_version}/man*/
rmdir man-pages-ru_%{mpr_version}

# remove .so links to nonexisting pages
for mdir in $(ls ./ | grep man); do
  for mfile in $(find $mdir/*.[0-9] -size 1); do
    if [ $(wc -l $mfile | sed 's| .*||') -eq 1 ]; then
      so_link=$(sed 's|.so ||' $mfile);
      if ( ! [ -e $so_link ] ); then
        rm $mfile
      fi
    fi
  done
done

%build

%install
rm -fr $RPM_BUILD_ROOT
iconv -f koi8-r -t UTF-8 < NEWS > NEWS.new
mv -f NEWS.new NEWS
for i in man*/*; do
        iconv -f koi8-r -t UTF-8 < $i > $i.new
        mv -f $i.new $i
done
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
LC_ALL=ru_RU make install INSTALLPATH=$RPM_BUILD_ROOT/%{_mandir} \
    LANG_SUBDIR=ru

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc NEWS README License
%dir %{_mandir}/ru
%{_mandir}/ru/*


%changelog
* Tue May 11 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.97-9
- Resolves: #589513
  add new source (Source1)

* Tue Feb 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.97-8
- Resolves: #543948
  minor spec file changes

* Mon Dec 21 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 0.97-7
- Resolves: #548697
  fix source tag

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.97-6.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.97-4
- fix license tag

* Mon Jun 16 2008 Ivana Varekova <varekova@redhat.com> - 0.97-3
- rebuild
- change license tag

* Fri Mar  2 2007 Ivana Varekova <varekova@redhat.com> - 0.97-2
- Resolves: 226129
  incorporate package review feedback

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.97-1.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Oct 21 2004 Adrian Havill <havill@redhat.com> 0.97-1
- Russian translation project active again; newest update merged with
  working Makefile (#131659)

* Wed Sep 29 2004 Elliot Lee <sopwith@redhat.com> 0.7-8
- Rebuild

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 11 2003 Phil Knirsch <pknirsch@redhat.com> 0.7-6
- Convert all manpages to utf-8.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.7-5
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 0.7-4
- rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.7-1
- 0.7

* Thu Aug  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- s/Copyright/License/
- Own %%{_mandir}/ru

* Wed Apr  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- roff fixes

* Mon Feb  5 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Version 0.6

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 20 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to compress man pages.

* Sun Jun 11 2000 Trond Eivind Glomsrød <teg@redhat.com>
- first build
