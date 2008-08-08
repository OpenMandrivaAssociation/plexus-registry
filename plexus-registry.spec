# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 0
# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'
%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define section     free

%define namedversion 1.0-alpha-3

%define parent plexus
%define subname registry

Name:           plexus-registry
Version:        1.0
Release:        %mkrel 2.a3.1.0.1
Epoch:          0
Summary:        Plexus Registry Component
License:        Apache Software License 2.0
Group:          Development/Java
URL:            http://plexus.codehaus.org/
Source0:        %{name}-%{namedversion}.tar.gz
# svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-registry-1.0-alpha-3/

Source2:        plexus-registry-settings.xml
Source3:        plexus-registry-1.0-jpp-depmap.xml
Source4:        plexus-registry-api-build.xml
Source5:        plexus-registry-commons-build.xml
Source6:        plexus-registry-naming-build.xml
Source7:        plexus-registry-test-build.xml

Patch0:         plexus-registry-commons-pom.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRequires:  jpackage-utils >= 0:1.7.3
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit
BuildRequires:  junit
BuildRequires:  hsqldb
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-release
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-surefire
BuildRequires:  plexus-maven-plugin
%endif
BuildRequires:  directory-naming
BuildRequires:  avalon-framework
BuildRequires:  geronimo-javamail-1.3.1-api
BuildRequires:  jakarta-commons-beanutils
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-configuration
BuildRequires:  jakarta-commons-digester
BuildRequires:  jakarta-commons-lang
BuildRequires:  jakarta-commons-logging
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-component-api 
BuildRequires:  plexus-containers-container-default 
BuildRequires:  plexus-naming 
BuildRequires:  plexus-utils 

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif
Requires:  directory-naming
Requires:  jakarta-commons-configuration
Requires:  jakarta-commons-lang
Requires:  plexus-classworlds
Requires:  plexus-containers-component-api 
Requires:  plexus-containers-container-default 
Requires:  plexus-naming 
Requires:  plexus-utils 

Requires(post):    jpackage-utils >= 0:1.7.3
Requires(postun):  jpackage-utils >= 0:1.7.3

%description
The Plexus project seeks to create end-to-end developer tools for 
writing applications. At the core is the container, which can be 
embedded or for a full scale application server. There are many 
reusable components for hibernate, form processing, jndi, i18n, 
velocity, etc. Plexus also includes an application server which 
is like a J2EE application server, without all the baggage.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
cp %{SOURCE2} settings.xml

cp %{SOURCE4}        plexus-registry-api/build.xml
cp %{SOURCE5}        plexus-registry-providers/plexus-registry-commons/build.xml
cp %{SOURCE6}        plexus-registry-providers/plexus-registry-naming/build.xml
cp %{SOURCE7}        plexus-registry-test/build.xml
%patch0 -b .sav0

%build
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

%if %{with_maven}
    mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven.test.failure.ignore=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE3} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%else
export CLASSPATH=$(build-classpath \
commons-beanutils \
commons-collections \
commons-configuration \
commons-lang \
commons-logging \
directory-naming/naming-config \
directory-naming/naming-core \
directory-naming/naming-java \
junit \
plexus/classworlds \
plexus/containers-component-api \
plexus/containers-container-default \
plexus/naming \
plexus/utils \
)
CLASSPATH=$CLASSPATH:$(pwd)/plexus-registry-api/target/plexus-registry-api-%{namedversion}.jar
CLASSPATH=$CLASSPATH:$(pwd)/plexus-registry-test/target/plexus-registry-test-%{namedversion}.jar
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
pushd plexus-registry-api
%ant -Dbuild.sysclasspath=only jar javadoc
popd
pushd plexus-registry-test
%ant -Dbuild.sysclasspath=only jar javadoc
popd
pushd plexus-registry-providers/plexus-registry-commons
%ant -Dbuild.sysclasspath=only jar javadoc
popd
pushd plexus-registry-providers/plexus-registry-naming
%ant -Dbuild.sysclasspath=only jar javadoc
popd

%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus

install -pm 644 %{name}-api/target/%{name}-api-%{namedversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/%{subname}-api-%{version}.jar
%add_to_maven_depmap org.codehaus.plexus %{name}-api %{version} JPP/%{parent} %{subname}-api
install -pm 644 %{name}-providers/%{name}-commons/target/%{name}-commons-%{namedversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/%{subname}-commons-%{version}.jar
%add_to_maven_depmap org.codehaus.plexus %{name}-naming %{version} JPP/%{parent} %{subname}-naming
install -pm 644 %{name}-providers/%{name}-naming/target/%{name}-naming-%{namedversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/%{subname}-naming-%{version}.jar
%add_to_maven_depmap org.codehaus.plexus %{name}-naming %{version} JPP/%{parent} %{subname}-naming
install -pm 644 %{name}-test/target/%{name}-test-%{namedversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/%{subname}-test-%{version}.jar
%add_to_maven_depmap org.codehaus.plexus %{name}-test %{version} JPP/%{parent} %{subname}-test

(cd $RPM_BUILD_ROOT%{_javadir}/plexus && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}.pom
install -pm 644 %{name}-api/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}-api.pom
install -pm 644 %{name}-test/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}-test.pom
install -pm 644 %{name}-providers/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}-providers.pom
install -pm 644 %{name}-providers/%{name}-commons/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}-commons.pom
install -pm 644 %{name}-providers/%{name}-naming/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}-naming.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
cp -pr %{name}-api/target/site/apidocs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/commons
cp -pr %{name}-providers/%{name}-commons/target/site/apidocs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/commons
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/naming
cp -pr %{name}-providers/%{name}-naming/target/site/apidocs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/naming
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/test
cp -pr %{name}-test/target/site/apidocs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/test
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%{_javadir}/%{parent}/*
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
