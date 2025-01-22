#include "clang/AST/ASTConsumer.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/AST/ASTContext.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Frontend/FrontendAction.h"
#include "clang/Frontend/ASTConsumers.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"

#include <iostream>
#include <string>
#include <vector>

using namespace clang;
using namespace clang::tooling;
using namespace llvm;

static cl::OptionCategory MyToolCategory("my-tool options");
static cl::opt<std::string> TargetVariable("var", cl::Required, cl::desc("Target variable to find usage"), cl::cat(MyToolCategory));

class MyASTVisitor : public RecursiveASTVisitor<MyASTVisitor> {
public:
  bool VisitDeclRefExpr(DeclRefExpr* E) {
    if (std::find(targetVariables.begin(), targetVariables.end(), E->getNameInfo().getAsString()) != targetVariables.end()) {
      if(VarDecl *VD = dyn_cast<VarDecl>(E->getDecl())){
      llvm::errs() << "Variable used in line: " << currentSourceManager->getSpellingLineNumber(E->getLocation()) << "\n";
       llvm::outs() << "VarDecl Name: " << VD->getNameAsString() << "\n";
      }
    }
    return true;
  }

  std::string getCurrentFunctionName() {
    return currentFunctionName;
  }

  bool VisitMemberExpr(MemberExpr* E) {

  Expr* base = E->getBase();
  if (DeclRefExpr* DRE = dyn_cast<DeclRefExpr>(base)) {
    std::string structName = DRE->getNameInfo().getAsString();

    std::string memberName = E->getMemberNameInfo().getAsString();

    std::string fullName = structName + "." + memberName;

    if (std::find(targetVariables.begin(), targetVariables.end(), fullName) != targetVariables.end()) {
      llvm::errs() << "Variable used in function: " << currentSourceManager->getSpellingLineNumber(E->getLocation()) << "\n";
    }
  }
  return true;
}

  void setSourceManager(SourceManager* SM) {
    currentSourceManager = SM;
  }

  void setCurrentLocation(SourceLocation loc) {
    currentSourceLocation = loc;
  }

  void setTargetVariables(const std::vector<std::string>& targetVars) {
    targetVariables = targetVars;
  }

private:
  std::string currentFunctionName = "";
  SourceManager* currentSourceManager = nullptr;
  SourceLocation currentSourceLocation;
  std::vector<std::string> targetVariables;
};

class MyASTConsumer : public ASTConsumer {
public:
  MyASTConsumer() : visitor() {}

  void HandleTranslationUnit(ASTContext& context) override {
    visitor.setTargetVariables({ TargetVariable });
    const FunctionDecl* FD = nullptr;
      for (const Decl* D : context.getTranslationUnitDecl()->decls()) {
          if (const auto* Function = dyn_cast<FunctionDecl>(D)) {
              FD = Function;
              break;
      }
}
    SourceLocation loc = FD->getLocation();
    visitor.setCurrentLocation(loc);
    visitor.setSourceManager(&context.getSourceManager());
    visitor.TraverseDecl(context.getTranslationUnitDecl());
  }

private:
  MyASTVisitor visitor;
};

class MyFrontendAction : public ASTFrontendAction {
public:
  std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance& compilerInstance, StringRef file) override {
    return std::unique_ptr<ASTConsumer>(new MyASTConsumer);
  }
};

int main(int argc, const char* argv[]) {

  auto optionsParser = CommonOptionsParser::create(argc, argv, MyToolCategory);
  ClangTool tool(optionsParser->getCompilations(), optionsParser->getSourcePathList());
  int result = tool.run(newFrontendActionFactory<MyFrontendAction>().get());

  return result;
}
