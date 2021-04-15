#! /bin/bash
TARGET_DIR=$1

if [ "$#" -ne 1 ]; then
    echo "usage: clone.sh TARGET_DIR"
    exit
fi

mkdir -p $TARGET_DIR
cd $TARGET_DIR

git clone https://github.com/JetBrains/kotlin kotlin
git clone https://github.com/apache/groovy groovy
git clone https://github.com/lampepfl/dotty dotty
git clone https://github.com/scala/scala scala
git clone https://github.com/openjdk/valhalla valhalla
hg clone http://hg.openjdk.java.net/type-annotations/type-annotations/ type-annotations
cd type-annotations && bash get_source.sh; cd ..
hg clone http://hg.openjdk.java.net/jdk/jdk/ jdk
cd jdk && bash get_source.sh; cd ..
hg clone http://hg.openjdk.java.net/jdk7/jdk7/ jdk7
cd jdk7 && bash get_source.sh; cd ..
hg clone http://hg.openjdk.java.net/jdk7u/jdk7u/ jdk7u
cd jdk7u && bash get_source.sh; cd ..
hg clone http://hg.openjdk.java.net/jdk8/jdk8/ jdk8
cd jdk8 && bash get_source.sh; cd ..
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u/ jdk8u
cd jdk8u && bash get_source.sh; cd ..
hg clone http://hg.openjdk.java.net/jdk9/jdk9/ jdk9
cd jdk9 && bash get_source.sh; cd ..
hg clone http://hg.openjdk.java.net/jdk10/master/ jdk10
cd jdk10 && bash get_source.sh; cd ..
hg clone http://hg.openjdk.java.net/jdk/jdk13/ jdk13
cd jdk13 && bash get_source.sh; cd ..
hg clone http://hg.openjdk.java.net/jdk/jdk14/ jdk14
cd jdk14 && bash get_source.sh; cd ..
