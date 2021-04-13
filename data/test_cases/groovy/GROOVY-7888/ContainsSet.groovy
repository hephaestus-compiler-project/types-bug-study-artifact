class ContainsSet {
    private Set<File> files = new HashSet<File>()
    Set<File> getFiles() { files }
    void setFiles(Set<File> files) { this.files = files }
}
def modifyIdeaModel(ContainsSet set, File foo) {
    set.files += foo
}
def cs = new ContainsSet()
modifyIdeaModel(cs, new File('foo'))
assert cs.files.size() == 1
