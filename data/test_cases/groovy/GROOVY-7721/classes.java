interface I {
    R[] method();
}

interface I2 extends I {
    R2[] method();
}

interface R {}
interface R2 extends R {}
