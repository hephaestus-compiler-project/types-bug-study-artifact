class A{
        public int compareTo(Object o){
                return 0;
        }
}

class B extends A implements Comparable<B>{
        public int compareTo(B b){
                return 0;
        }

        public static void main(String[] argv){
                System.out.println(new B().compareTo(new Object(){}));
        }
}
