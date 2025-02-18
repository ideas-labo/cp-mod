package org.example.parser;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class functionsearch {
    public static void main(String[] args) {
        String filePath = "java file path (.java) ";
        String functionName = "Your functionname";
        List<String> results = new ArrayList<>();

        try (FileInputStream in = new FileInputStream(filePath);
             FileWriter csvWriter = new FileWriter("./function_results.csv")) {

            JavaParser javaParser = new JavaParser();
            ParseResult<CompilationUnit> parseResult = javaParser.parse(in);

            if (parseResult.isSuccessful()) {
                CompilationUnit cu = parseResult.getResult().get();

                cu.accept(new VoidVisitorAdapter<Void>() {
                    @Override
                    public void visit(MethodDeclaration methodDecl, Void arg) {
                        super.visit(methodDecl, arg);
                        if (methodDecl.getNameAsString().equals(functionName)) {
                            results.add(functionName + ",declared," + methodDecl.getRange().get().begin.line + "," + filePath);
                        }
                    }

                    @Override
                    public void visit(MethodCallExpr methodCall, Void arg) {
                        super.visit(methodCall, arg);
                        if (methodCall.getNameAsString().equals(functionName)) {
                            results.add(functionName + ",called," + methodCall.getRange().get().begin.line + "," + filePath);
                        }
                    }


                }, null);

                // Write results to CSV
                for (String result : results) {
                    csvWriter.append(result);
                    csvWriter.append("\n");
                }
            } else {
                System.out.println("Parsing failed for file: " + filePath);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
