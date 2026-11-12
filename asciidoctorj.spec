Name:		asciidoctorj
Version:	3.0.1
Release:	1
Summary:	AsciidoctorJ implementation used by Gradle's documentation build
Group:		Development/Java
License:	Apache-2.0 AND MIT AND BSD-2-Clause
URL:		https://github.com/asciidoctor/asciidoctorj
# Tag v3.0.1. gradle-wrapper.jar is removed from the lookaside.
Source0:	asciidoctorj-%{version}.tar.gz
# Asciidoctor 2.0.26 Ruby library. Tag v2.0.26. test/fixtures/assets.jar is removed.
Source1:	asciidoctor-2.0.26.tar.gz
# JRuby 9.4.14.0 default gems named by that tag's lib/pom.xml. The engine
# jar does not ship them. stringio and strscan are the JRuby Java extensions.
# cgi, uri, logger, and optparse are the Ruby files a standalone convert loads.
# C extensions in these tags are not compiled.
Source2:	stringio-3.1.5.tar.gz
Source3:	strscan-3.1.5.tar.gz
Source4:	cgi-0.3.7.tar.gz
Source5:	uri-0.12.4.tar.gz
Source6:	logger-1.5.1.tar.gz
Source7:	optparse-0.2.0.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
BuildRequires:	mvn(org.asciidoctor:asciidoctorj-api) = 3.0.1
BuildRequires:	mvn(org.jruby:jruby) = 9.4.14.0
BuildRequires:	mvn(org.ow2.asm:asm)
BuildRequires:	mvn(org.ow2.asm:asm-commons)
BuildRequires:	mvn(org.ow2.asm:asm-tree)
BuildRequires:	mvn(org.ow2.asm:asm-util)
BuildRequires:	mvn(com.github.jnr:jnr-netdb)
BuildRequires:	mvn(com.github.jnr:jnr-enxio)
BuildRequires:	mvn(com.github.jnr:jnr-unixsocket)
BuildRequires:	mvn(com.github.jnr:jnr-posix)
BuildRequires:	mvn(com.github.jnr:jnr-constants)
BuildRequires:	mvn(com.github.jnr:jnr-ffi)
BuildRequires:	mvn(com.github.jnr:jnr-a64asm)
BuildRequires:	mvn(com.github.jnr:jffi)
BuildRequires:	mvn(org.jruby.joni:joni)
BuildRequires:	mvn(org.jruby.jcodings:jcodings)
BuildRequires:	mvn(org.jruby:dirgra)
BuildRequires:	mvn(com.headius:invokebinder)
BuildRequires:	mvn(com.headius:options)
BuildRequires:	mvn(org.jruby:jzlib)
BuildRequires:	mvn(joda-time:joda-time)
BuildRequires:	mvn(me.qmx.jitescript:jitescript)
BuildRequires:	mvn(com.headius:backport9)
BuildRequires:	mvn(org.crac:crac)
BuildRequires:	mvn(org.apache.ant:ant)
BuildRequires:	mvn(org.osgi:org.osgi.core)
BuildRequires:	mvn(org.slf4j:slf4j-api)
Requires:	%{_sysjar_java_requires}

%description
AsciidoctorJ 3.0.1 is the Java implementation of org.asciidoctor:asciidoctorj.
Gradle 9.9.1's catalog names this coordinate. The jar is the core Java
sources, the Asciidoctor 2.0.26 library, and the JRuby default gems a
standalone HTML convert loads: stringio 3.1.5, strscan 3.1.5, cgi 0.3.7,
uri 0.12.4, logger 1.5.1, and optparse 0.2.0. Syntax-highlighter and
template gems are not included. package-info.java imports the OSGi Export
annotation, which cooker does not ship, so the build compiles a
CLASS-retention stub and leaves that stub out of the jar.

%prep
%setup -q -n asciidoctorj-%{version}
tar -xf %{SOURCE1}
tar -xf %{SOURCE2}
tar -xf %{SOURCE3}
tar -xf %{SOURCE4}
tar -xf %{SOURCE5}
tar -xf %{SOURCE6}
tar -xf %{SOURCE7}
cp -f asciidoctor-2.0.26/LICENSE LICENSE-asciidoctor.txt
cp -f stringio-3.1.5/LICENSE.txt LICENSE-stringio.txt
cp -f strscan-3.1.5/LICENSE.txt LICENSE-strscan.txt
cp -f cgi-0.3.7/LICENSE.txt LICENSE-cgi.txt
cp -f uri-0.12.4/LICENSE.txt LICENSE-uri.txt
cp -f logger-1.5.1/LICENSE.txt LICENSE-logger.txt
cp -f optparse-0.2.0/COPYING LICENSE-optparse.txt
if find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) | grep -q .; then
	echo 'prebuilt binaries remain' >&2
	find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \)
	exit 1
fi

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:$PATH"

cat > depjars.list << EOF
%{_javadir}/asm.jar
%{_javadir}/asm-commons.jar
%{_javadir}/asm-tree.jar
%{_javadir}/asm-util.jar
%{_javadir}/jnr-netdb.jar
%{_javadir}/jnr-enxio.jar
%{_javadir}/jnr-unixsocket.jar
%{_javadir}/jnr-posix.jar
%{_javadir}/jnr-constants.jar
%{_javadir}/jnr-ffi.jar
%{_javadir}/jnr-a64asm.jar
%{_javadir}/jffi.jar
%{_javadir}/joni.jar
%{_javadir}/jcodings.jar
%{_javadir}/dirgra.jar
%{_javadir}/invokebinder.jar
%{_javadir}/options.jar
%{_javadir}/jzlib.jar
%{_javadir}/joda-time.jar
%{_javadir}/jitescript.jar
%{_javadir}/backport9.jar
%{_javadir}/crac.jar
%{_javadir}/ant.jar
%{_javadir}/org.osgi.core.jar
%{_javadir}/slf4j-api.jar
EOF
CP=%{_javadir}/jruby.jar:%{_javadir}/asciidoctorj-api.jar
while IFS= read -r jar; do
	test -s "$jar"
	CP="$CP:$jar"
done < depjars.list

mkdir -p classes stub/org/osgi/annotation/bundle stubclasses
cat > stub/org/osgi/annotation/bundle/Export.java << 'EOF'
package org.osgi.annotation.bundle;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
@Retention(RetentionPolicy.CLASS)
@Target(ElementType.PACKAGE)
public @interface Export {}
EOF
javac --release 11 -encoding UTF-8 -Xlint:-options -d stubclasses stub/org/osgi/annotation/bundle/Export.java

find stringio-3.1.5/ext/java strscan-3.1.5/ext/jruby cgi-0.3.7/ext/java -name '*.java' > ext.list
test "$(wc -l < ext.list)" -eq 5
javac --release 11 -encoding UTF-8 -Xlint:-options -cp "$CP" -d classes @ext.list
test -s classes/org/jruby/ext/stringio/StringIOLibrary.class
test -s classes/org/jruby/ext/strscan/StringScannerLibrary.class
test -s classes/org/jruby/ext/cgi/escape/CGIEscape.class

find asciidoctorj-core/src/main/java -name '*.java' > java.list
test "$(wc -l < java.list)" -eq 77
javac -encoding UTF-8 -cp "$CP:stubclasses" -d classes @java.list
test -s classes/org/asciidoctor/jruby/internal/JRubyAsciidoctor.class
if find classes -name 'Export.class' | grep -q .; then
	echo 'osgi stub leaked into classes' >&2
	exit 1
fi

cp -a asciidoctorj-core/src/main/resources/. classes/
mkdir -p classes/gems/asciidoctor-2.0.26 classes/specifications classes/cgi classes/strscan
cp -a asciidoctor-2.0.26/lib asciidoctor-2.0.26/data classes/gems/asciidoctor-2.0.26/
cp -a uri-0.12.4/lib/. classes/
cp -a logger-1.5.1/lib/. classes/
cp -a optparse-0.2.0/lib/. classes/
cp -f cgi-0.3.7/lib/cgi/util.rb classes/cgi/util.rb
cp -f strscan-3.1.5/lib/strscan/strscan.rb classes/strscan/strscan.rb
cat > classes/stringio.rb << 'EOF'
JRuby::Util.load_ext("org.jruby.ext.stringio.StringIOLibrary")
EOF
cat > classes/strscan.rb << 'EOF'
JRuby::Util.load_ext("org.jruby.ext.strscan.StringScannerLibrary")
require "strscan/strscan"
EOF
cat > classes/cgi/escape.rb << 'EOF'
JRuby::Util.load_ext("org.jruby.ext.cgi.escape.CGIEscape")
EOF
cat > classes/specifications/asciidoctor-2.0.26.gemspec << 'EOF'
Gem::Specification.new do |s|
  s.name = "asciidoctor"
  s.version = "2.0.26"
  s.authors = ["Dan Allen"]
  s.summary = "Asciidoctor"
  s.license = "MIT"
  s.files = []
  s.require_paths = ["lib"]
end
EOF
test -s classes/META-INF/services/org.asciidoctor.Asciidoctor
test -s classes/gems/asciidoctor-2.0.26/lib/asciidoctor.rb
test -s classes/gems/asciidoctor-2.0.26/data/stylesheets/asciidoctor-default.css
test -s classes/logger.rb
test -s classes/optparse.rb
test -s classes/uri.rb
test -s classes/cgi/util.rb
test -s classes/strscan/strscan.rb
if grep -F -q 'stringio.jar' classes/stringio.rb; then
	echo 'stringio loader still asks for a jar' >&2
	exit 1
fi
if grep -F -q 'strscan.jar' classes/strscan.rb; then
	echo 'strscan loader still asks for a jar' >&2
	exit 1
fi
if find classes -type f \( -name '*.jar' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) | grep -q .; then
	echo 'binary slipped into classes' >&2
	exit 1
fi

cat > manifest.mf << 'EOF'
Manifest-Version: 1.0
Automatic-Module-Name: org.asciidoctor.asciidoctorj

EOF
jar cfm asciidoctorj.jar manifest.mf -C classes .
jar i asciidoctorj.jar
javap -verbose -cp asciidoctorj.jar org.asciidoctor.jruby.internal.JRubyAsciidoctor | grep -F 'major version: 71'
jar --describe-module -f asciidoctorj.jar > describe.txt
grep -F -q 'org.asciidoctor.asciidoctorj' describe.txt
grep -F -q 'provides org.asciidoctor.Asciidoctor with org.asciidoctor.jruby.internal.JRubyAsciidoctor' describe.txt
if grep -F -q 'Unable' describe.txt; then
	cat describe.txt
	exit 1
fi

cat > asciidoctorj.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.asciidoctor</groupId>
  <artifactId>asciidoctorj</artifactId>
  <version>%{version}</version>
  <name>asciidoctorj</name>
  <description>AsciidoctorJ implementation</description>
  <licenses>
    <license>
      <name>Apache-2.0</name>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>org.asciidoctor</groupId>
      <artifactId>asciidoctorj-api</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jruby</groupId>
      <artifactId>jruby</artifactId>
      <version>9.4.14.0</version>
    </dependency>
  </dependencies>
</project>
EOF

%install
set -eo pipefail
sysjar install --buildroot %{buildroot} \
	--artifact asciidoctorj.pom:asciidoctorj.jar \
	--file-name asciidoctorj \
	--filelist .mfiles
idx="%{buildroot}/usr/share/sysjar/index/org.asciidoctor/asciidoctorj.sysjar"
test -s "$idx"
grep -F -q '"version": "%{version}"' "$idx"
grep -F -q '"artifactId": "asciidoctorj"' "$idx"
test -s %{buildroot}%{_javadir}/asciidoctorj.jar

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:$PATH"
JAR=%{buildroot}%{_javadir}/asciidoctorj.jar
test -s "$JAR"
CP="$JAR:%{_javadir}/asciidoctorj-api.jar:%{_javadir}/jruby.jar"
while IFS= read -r dep; do
	test -s "$dep"
	CP="$CP:$dep"
done < depjars.list
mkdir -p check
cat > check/Smoke.java << 'EOF'
import org.asciidoctor.Asciidoctor;
import org.asciidoctor.Options;
public class Smoke {
    public static void main(String[] args) {
        Asciidoctor doctor = Asciidoctor.Factory.create();
        String html = doctor.convert("= Hello\n\nworld", Options.builder().standalone(true).build());
        String version = doctor.asciidoctorVersion();
        if (html == null || !html.contains("<h1>Hello</h1>") || !html.contains("world")) {
            System.out.println(html);
            throw new RuntimeException("missing document");
        }
        if (!"2.0.26".equals(version)) {
            throw new RuntimeException("version " + version);
        }
        System.out.println("asciidoctorj_ok " + version);
        doctor.shutdown();
    }
}
EOF
"$JAVA_HOME/bin/javac" --release 11 -encoding UTF-8 -Xlint:-options -cp "%{_javadir}/asciidoctorj-api.jar" -d check check/Smoke.java
"$JAVA_HOME/bin/java" \
	--enable-native-access=ALL-UNNAMED \
	-Djffi.boot.library.path=%{_libdir} \
	-Djava.library.path=%{_libdir} \
	--add-exports jdk.unsupported/sun.misc=ALL-UNNAMED \
	--add-opens java.base/java.lang=ALL-UNNAMED \
	--add-opens java.base/java.io=ALL-UNNAMED \
	--add-opens java.base/java.util=ALL-UNNAMED \
	--add-opens java.base/sun.nio.ch=ALL-UNNAMED \
	-cp "check:$CP" \
	Smoke > check/out.txt
cat check/out.txt
grep -F -qx 'asciidoctorj_ok 2.0.26' check/out.txt

%files -f .mfiles
%doc README.adoc
%license LICENSE.txt LICENSE-asciidoctor.txt LICENSE-stringio.txt LICENSE-strscan.txt LICENSE-cgi.txt LICENSE-uri.txt LICENSE-logger.txt LICENSE-optparse.txt
