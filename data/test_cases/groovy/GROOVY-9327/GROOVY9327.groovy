def method() {
    new Runnable() {
        @Override
        void run() {
            foo // invalid reference
        }
    }
}
