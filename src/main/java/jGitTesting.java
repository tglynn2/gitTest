import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.api.errors.NoFilepatternException;
import org.eclipse.jgit.transport.UsernamePasswordCredentialsProvider;

import java.io.File;
import java.io.IOException;

public class jGitTesting {

    public static void main(String[] args) {
        try {
            // Initialize the repository
            File repoDir = new File("/path/to/my-git-repo");
            Git git = Git.open(repoDir);

            // Path to the file to be added
            File newFile = new File(repoDir, "example.txt");
            if (!newFile.exists()) {
                newFile.createNewFile(); // Create a new file
            }

            // Add the file to the repository
            git.add().addFilepattern("example.txt").call();

            // Commit the changes
            git.commit().setMessage("Added example.txt").call();

            // Push the changes (optional, if you have a remote repo setup)
            git.push()
                    .setCredentialsProvider(new UsernamePasswordCredentialsProvider("your-username", "your-password"))
                    .call();

            System.out.println("File uploaded to Git repo!");

        } catch (IOException | GitAPIException e) {
            e.printStackTrace();
        }
    }
}


