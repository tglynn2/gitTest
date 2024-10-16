public class libGitTest {
    static {
        System.loadLibrary("gitmanager");
    }


    public native void deleteFile(String repoPath, String filePath);
    public native void createFolder(String repoPath, String folderPath);


    public static void main(String[] args) {
        libGitTest prepWork = new libGitTest();
        prepWork.deleteFile("/path/to/repo", "file_to_delete.txt");
        prepWork.createFolder("/path/to/repo", "new_folder");
    }
}
