# main file

# ===== imports =====
import frontend
import backend

# ===== definitions =====

def readQuestion():
    return raw_input("Please enter a question: ")

# ===== main testing =====          
if __name__ == "__main__":
    mat, glove = backend.processPattyData()
    mat, maxLength = backend.padVectors(mat)
    vectors, _, _, _ = frontend.processQuestion(glove,readQuestion())
      
        
# Who is the wife of Obama