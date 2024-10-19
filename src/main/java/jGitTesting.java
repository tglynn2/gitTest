import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.transport.UsernamePasswordCredentialsProvider;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.Properties;

public class jGitTesting {

    public static void main(String[] args) {
        String repoPath = "C:\\Users\\tommy\\IdeaProjects\\gitTesting";
        String filePath = "C:\\cygwin64\\home\\tommy\\322hw\\sortHw.py";
        String filePath2 = "C:\\cygwin64\\home\\tommy\\322hw\\sortHwCSV.py";
        String configFilePath = "config.properties";

        try {
            Properties props = loadConfig(configFilePath);
            String username = props.getProperty("username");
            String password = props.getProperty("password");

            uploadFile(repoPath, filePath2, username, password);
            deleteFile(repoPath, filePath, username, password);
            newFolder(repoPath, "testNewFolder", username, password);
        } catch (IOException | GitAPIException e) {
            e.printStackTrace();
        }
    }

    public static Properties loadConfig(String configFilePath) throws IOException {
        Properties props = new Properties();
        try (FileInputStream input = new FileInputStream(configFilePath)) {
            props.load(input);
        }
        return props;
    }

    public static void uploadFile(String repoPath, String filePath, String username, String password) throws IOException, GitAPIException {
        File repoDir = new File(repoPath);
        Git git = Git.open(repoDir);
        Path sourceFile = Path.of(filePath);
        Path destinationFile = Path.of(repoDir.getAbsolutePath(), sourceFile.getFileName().toString());
        Files.copy(sourceFile, destinationFile, StandardCopyOption.REPLACE_EXISTING);
        git.add().addFilepattern(sourceFile.getFileName().toString()).call();
        git.commit().setMessage("Added " + sourceFile.getFileName()).call();
        git.push()
                .setCredentialsProvider(new UsernamePasswordCredentialsProvider(username, password))
                .call();
        System.out.println("New folder created");
    }

    public static void newFolder(String repoPath, String folderName, String username, String password) throws IOException, GitAPIException {
        File repoDir = new File(repoPath);
        Git git = Git.open(repoDir);
        Path newDirec = Path.of(repoDir.getAbsolutePath(), folderName);
        Files.createDirectories(newDirec);
        Path placeholderFile = newDirec.resolve(".gitkeep");
        Files.createFile(placeholderFile);
        git.add().addFilepattern(folderName + "/.gitkeep").call();
        git.commit().setMessage("Created new folder " + folderName).call();
        git.push()
                .setCredentialsProvider(new UsernamePasswordCredentialsProvider(username, password))
                .call();
        System.out.println("File uploaded");
    }


    public static void deleteFile(String repoPath, String filePath, String username, String password) throws IOException, GitAPIException {
        File repoDir = new File(repoPath);
        Git git = Git.open(repoDir);
        Path sourceFile = Path.of(filePath);
        Path fileToDelete = Path.of(repoDir.getAbsolutePath(), sourceFile.getFileName().toString());
        Files.deleteIfExists(fileToDelete);
        git.add().addFilepattern(sourceFile.getFileName().toString()).call();
        git.commit().setMessage("Deleted " + sourceFile.getFileName()).call();
        git.push()
                .setCredentialsProvider(new UsernamePasswordCredentialsProvider(username, password))
                .call();
        System.out.println("File deleted");
    }
}
