# Don't try fancy stuff like debuginfo, which is useless on binary-only
# packages. Don't strip binary too
# Be sure buildpolicy set to do nothing
%define		__spec_install_post %{nil}
%define		debug_package %{nil}
%define		__os_install_post %{_dbpath}/brp-compress

Name:		sonarqube
Version:	6.7
Release:	1
Summary:	Open platform to manage code quality
Vendor:		SonarSource
Packager:	Evgeny Mandrikov <mandrikov@gmail.com>
Group:		Development/Tools
License:	LGPLv3
URL:		http://sonarsource.org/
Source:		sonarqube-6.7.1.zip
# wget https://sonarsource.bintray.com/Distribution/sonarqube/sonarqube-6.7.1.zip
# wget https://sonarsource.bintray.com/Distribution/sonarqube/sonarqube-6.7.1.zip.md5
Source1:	sonar.init.in
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:	
#Requires:	
BuildArch:	x86_64
Autoreq:	0
Autoprov:	0

%description
Sonar is an open source software quality management tool, dedicated
to continuously analyze and measure source code quality.

%prep
%setup -q -n sonarqube-6.7.1

%build

%install
rm -rf %{buildroot}

# Remove unnecessary files
rm -rv bin/windows*
# Removed from official distribution in 5.4:
rm -rv bin/solaris* || true
rm -rv bin/macosx*
# Removed from official distribution in 5.1:
rm -rv bin/linux-ppc* || true

# Fix EOL in configuration files
for i in conf/* ; do
  echo "dos2unix $i"
  awk '{ sub("\r$", ""); print }' $i > $i.new
  mv $i.new $i
done

mkdir -p %{buildroot}/opt/sonar/
cp -R %{_builddir}/sonarqube-6.7.1/* %{buildroot}/opt/sonar/

%__install -D -m0755 "%{SOURCE1}" "%{buildroot}/etc/init.d/%{name}"

%pre
/usr/sbin/groupadd -r sonar &>/dev/null || :
/usr/sbin/useradd -g sonar -s /bin/sh -r -d "/opt/sonar" sonar &>/dev/null || :

%post
/sbin/chkconfig --add sonar

%preun
if [ "$1" = 0 ] ; then
  # if this is uninstallation as opposed to upgrade, delete the service
  /sbin/service sonar stop > /dev/null 2>&1
  /sbin/chkconfig --del sonar
fi
exit 0

%clean
rm -rf %{buildroot}

%files
%defattr(0644,sonar,sonar,0755)
/opt/sonar
%config(noreplace) /opt/sonar/conf/sonar.properties

%attr(0755,sonar,sonar) /opt/sonar/bin/linux-x86-32/sonar.sh
%attr(0755,sonar,sonar) /opt/sonar/bin/linux-x86-32/wrapper
%attr(0755,sonar,sonar) /opt/sonar/bin/linux-x86-32/lib/libwrapper.so

%attr(0755,sonar,sonar) /opt/sonar/bin/linux-x86-64/sonar.sh
%attr(0755,sonar,sonar) /opt/sonar/bin/linux-x86-64/wrapper
%attr(0755,sonar,sonar) /opt/sonar/bin/linux-x86-64/lib/libwrapper.so

%attr(0755,sonar,sonar) /opt/sonar/elasticsearch/bin/elasticsearch

%attr(0755,root,root) %config /etc/init.d/%{name}
