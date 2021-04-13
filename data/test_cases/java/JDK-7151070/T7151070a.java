class T7151070a {
    private static class PrivateCls { }
    public static class PublicCls extends PrivateCls { }

    public void m(PrivateCls p) { }
}
