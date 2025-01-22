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
static cl::opt<std::string> FuncionName("name", cl::Required, cl::desc("search field function"),cl::cat(MyToolCategory));
static cl::opt<std::string> Targets("fun", cl::Required, cl::desc("search target"), cl::cat(MyToolCategory));


class funVisitor : public RecursiveASTVisitor<funVisitor> {
public:
  explicit funVisitor(ASTContext *Context) : Context(Context) {}

  bool VisitDeclRefExpr(DeclRefExpr* E) {
    if (std::find(targets.begin(), targets.end(), E->getNameInfo().getAsString()) != targets.end()) {
      llvm::outs() << "Detected:" << E->getNameInfo().getAsString() << " at line:" << E->getBeginLoc().printToString(Context->getSourceManager()) << "\n";
    }
    return true;
  }

 void setTargets(const std::vector<std::string>& targetVars) {
    targets = targetVars;
  }
private:
  ASTContext *Context;
  std::vector<std::string> targets;
};


class LoopASTConsumer : public ASTConsumer {
public:
  explicit LoopASTConsumer(ASTContext *Context, const std::string &FunctionName ,const std::string &Targets) : Visitor(Context), FunctionName(FunctionName) {}


  bool HandleTopLevelDecl(DeclGroupRef DG) override {
    Visitor.setTargets({ Targets });
    for (Decl *D : DG) {
      if (FunctionDecl *FD = dyn_cast<FunctionDecl>(D)) {

        if (FD->getNameAsString() == FunctionName) {
          Visitor.TraverseDecl(D);
        }
      }
    }
    return true;
  }

private:
  funVisitor Visitor;
  std::string FunctionName;
};

class MyFrontendAction : public ASTFrontendAction {
public:
  std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &compilerInstance, StringRef file) override {
    ASTContext &context = compilerInstance.getASTContext();
    return std::unique_ptr<ASTConsumer>(new LoopASTConsumer(&context,FuncionName,Targets));
  }
};


int main(int argc, const char **argv) {

  auto optionsParser = CommonOptionsParser::create(argc, argv,MyToolCategory);
  ClangTool Tool(optionsParser->getCompilations(), optionsParser->getSourcePathList());

Tool.run(newFrontendActionFactory<MyFrontendAction>().get());

  return 0;
}

