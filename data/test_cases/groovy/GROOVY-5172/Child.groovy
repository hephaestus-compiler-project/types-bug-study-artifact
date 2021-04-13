class Child extends GroovyPage {
                void foo() {
                    createTagBody(1) { ->
                        printHtmlPart(2)
                    }
                }
            }