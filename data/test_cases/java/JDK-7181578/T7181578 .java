class T7181578 {
    String test(boolean cond) {
        final String s;
        try {
            if (cond) {
                try {
                    s = "";
                    return s;
                } finally { }
            } else {
                s = "";
            }
            return s; // bug occurs here: mapping is always initialized
        } finally { }
    }
}