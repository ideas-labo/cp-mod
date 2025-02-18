package org.example.parser;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class varsearch {
    public static void main(String[] args) {
        String filePath = "java file path (.java) ";
        String variableName = "Your variableName";
        List<String> results = new ArrayList<>();

        try (FileInputStream in = new FileInputStream(filePath);
             FileWriter csvWriter = new FileWriter("./variable_results.csv")) {

            JavaParser javaParser = new JavaParser();
            ParseResult<CompilationUnit> parseResult = javaParser.parse(in);

            if (parseResult.isSuccessful()) {
                CompilationUnit cu = parseResult.getResult().get();

                cu.accept(new VoidVisitorAdapter<Void>() {
                    @Override
                    public void visit(VariableDeclarator varDeclarator, Void arg) {
                        super.visit(varDeclarator, arg);
                        if (varDeclarator.getNameAsString().equals(variableName)) {
                            results.add(variableName + ",declared," + varDeclarator.getRange().get().begin.line + "," + filePath);
                        }
                    }

                    @Override
                    public void visit(NameExpr nameExpr, Void arg) {
                        super.visit(nameExpr, arg);
                        if (nameExpr.getNameAsString().equals(variableName)) {
                            results.add(variableName + ",used," + nameExpr.getRange().get().begin.line + "," + filePath);
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
