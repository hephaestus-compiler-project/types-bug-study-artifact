interface fint { int get(); }

@interface atype {
  fint fld = ()->(fld==null?0:1);
}

@atype class T {}
