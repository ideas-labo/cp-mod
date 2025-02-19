#include <iostream>
#include <string>
#include "clang/AST/AST.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
#include "clang/Frontend/CompilerInstance.h"

using namespace clang;
using namespace clang::tooling;
using namespace llvm;

static cl::OptionCategory MyToolCategory("my-tool options");
static cl::opt<std::string> FunctionName("name", cl::Required, cl::desc("Function to search for"), cl::cat(MyToolCategory));
static cl::opt<std::string> FileName("file", cl::Required, cl::desc("File to search in"), cl::cat(MyToolCategory));


class FunctionCallVisitor : public RecursiveASTVisitor<FunctionCallVisitor> {
public:
  explicit FunctionCallVisitor(ASTContext *Context, const std::string &TargetFunction) 
    : Context(Context), TargetFunction(TargetFunction) {}

  bool VisitCallExpr(CallExpr *E) {
    if (E->getDirectCallee() && E->getDirectCallee()->getNameAsString() == TargetFunction) {
      SourceLocation StartLoc = E->getBeginLoc();
      llvm::outs() << "Function '" << TargetFunction << "' called at line: "
                   << Context->getSourceManager().getSpellingLineNumber(StartLoc) << "\n";
    }
    return true;
  }

private:
  ASTContext *Context;
  std::string TargetFunction;
};


class FunctionCallASTConsumer : public ASTConsumer {
public:
  explicit FunctionCallASTConsumer(ASTContext *Context, const std::string &FunctionName) 
    : Visitor(Context, FunctionName) {}

  bool HandleTopLevelDecl(DeclGroupRef DG) override {
    for (Decl *D : DG) {
      Visitor.TraverseDecl(D);
    }
    return true;
  }

private:
  FunctionCallVisitor Visitor;
};

class MyFrontendAction : public ASTFrontendAction {
public:
  std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &compilerInstance, StringRef inFile) override {
    ASTContext &context = compilerInstance.getASTContext();
    return std::make_unique<FunctionCallASTConsumer>(&context, FunctionName);
  }
};


int main(int argc, const char **argv) {

  auto optionsParser = CommonOptionsParser::create(argc, argv, MyToolCategory);
  ClangTool Tool(optionsParser->getCompilations(), optionsParser->getSourcePathList());

  Tool.run(newFrontendActionFactory<MyFrontendAction>().get());

  return 0;
}
