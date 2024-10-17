import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.transport.UsernamePasswordCredentialsProvider;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public class jGitTesting {
    public static void main(String[] args) {
        try {
            File repoDir = new File("C:\\Users\\tommy\\IdeaProjects\\gitTesting");
            Git git = Git.open(repoDir);
            Path sourceFile = Path.of("C:\\cygwin64\\home\\tommy\\322hw\\myCopy.c");
            Path destinationFile = Path.of(repoDir.getAbsolutePath(), "myCopy.c");
            Files.copy(sourceFile, destinationFile, StandardCopyOption.REPLACE_EXISTING);
            git.add().addFilepattern("myCopy.c").call();
            git.commit().setMessage("Added myCopy.c").call();
            git.push()
                    .setCredentialsProvider(new UsernamePasswordCredentialsProvider("tglynn2", "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"))
                    .call();
            System.out.println("File uploaded to Git repo!");
        }
        catch (IOException | GitAPIException e) {
            e.printStackTrace();
        }
    }
}
