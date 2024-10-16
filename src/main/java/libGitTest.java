public class libGitTest {
    static {
        System.loadLibrary("gitmanager");
    }


    public native void deleteFile(String repoPath, String filePath);
    public native void createFolder(String repoPath, String folderPath);


    public static void main(String[] args) {
        libGitTest prepWork = new libGitTest();
        prepWork.deleteFile("C:\\Users\\tommy\\IdeaProjects\\gitTesting", "analyzingSorts.py");
        prepWork.createFolder("C:\\Users\\tommy\\IdeaProjects\\gitTesting", "new_folder");
    }
}
