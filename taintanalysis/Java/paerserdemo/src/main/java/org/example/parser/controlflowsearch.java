package org.example.parser;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.stmt.*;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class controlflowsearch {
    public static void main(String[] args) {

        String folderPath = "Your target folder";
        List<JavaFileInfo> javaFiles = new ArrayList<>();
        listJavaFiles(new File(folderPath), javaFiles);

        JavaParser javaParser = new JavaParser();

        try (FileWriter controlFlowWriter = new FileWriter("./controlflow_results.csv");
             ) {

            for (JavaFileInfo fileInfo : javaFiles) {
                try (FileInputStream inputStream = new FileInputStream(fileInfo.getFile())) {
                    ParseResult<CompilationUnit> parseResult = javaParser.parse(inputStream);

                    if (parseResult.isSuccessful()) {
                        CompilationUnit cu = parseResult.getResult().get();

                        ControlFlowVisitor controlFlowVisitor = new ControlFlowVisitor(fileInfo, controlFlowWriter);
                        controlFlowVisitor.visit(cu, null);

                        // Assuming you want to track function declarations and calls as well,
                        // you'd need to implement another visitor for this purpose, but for brevity:
                        // FunctionVisitor functionVisitor = new FunctionVisitor(fileInfo, functionWriter);
                        // functionVisitor.visit(cu, null);

                    } else {
                        System.out.println("Parsing failed for file " + fileInfo.getName() + ": " + parseResult.getProblems());
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void listJavaFiles(File folder, List<JavaFileInfo> javaFiles) {
        File[] files = folder.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isFile() && file.getName().endsWith(".java")) {
                    javaFiles.add(new JavaFileInfo(file));
                } else if (file.isDirectory()) {
                    listJavaFiles(file, javaFiles);
                }
            }
        }
    }

    private static class JavaFileInfo {
        private File file;

        public JavaFileInfo(File file) {
            this.file = file;
        }

        public File getFile() {
            return file;
        }

        public String getName() {
            return file.getName();
        }

        public String getPath() {
            return file.getPath();
        }
    }

    private static class ControlFlowVisitor extends VoidVisitorAdapter<Void> {
        private JavaFileInfo fileInfo;
        private BufferedWriter writer;

        public ControlFlowVisitor(JavaFileInfo fileInfo, Writer writer) {
            this.fileInfo = fileInfo;
            this.writer = new BufferedWriter(writer);
        }

        private void writeControlFlowInfo(String controlFlowType, int startLine, int endLine) throws IOException {
            writer.write(String.format("%s,%s,%d,%d\n", fileInfo.getPath(), controlFlowType, startLine, endLine));
        }

        @Override
        public void visit(IfStmt ifStmt, Void arg) {
            super.visit(ifStmt, arg);
            try {
                writeControlFlowInfo("if", ifStmt.getRange().get().begin.line, ifStmt.getRange().get().end.line);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void visit(TryStmt tryStmt, Void arg) {
            super.visit(tryStmt, arg);
            try {
                writeControlFlowInfo("trycatch", tryStmt.getRange().get().begin.line, tryStmt.getRange().get().end.line);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void visit(WhileStmt whileStmt, Void arg) {
            super.visit(whileStmt, arg);
            try {
                writeControlFlowInfo("while", whileStmt.getRange().get().begin.line, whileStmt.getRange().get().end.line);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void visit(ForStmt forStmt, Void arg) {
            super.visit(forStmt, arg);
            try {
                writeControlFlowInfo("for", forStmt.getRange().get().begin.line, forStmt.getRange().get().end.line);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void visit(DoStmt doStmt, Void arg) {
            super.visit(doStmt, arg);
            try {
                writeControlFlowInfo("dowhile", doStmt.getRange().get().begin.line, doStmt.getRange().get().end.line);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void visit(SwitchStmt switchStmt, Void arg) {
            super.visit(switchStmt, arg);
            try {
                writeControlFlowInfo("switch", switchStmt.getRange().get().begin.line, switchStmt.getRange().get().end.line);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
