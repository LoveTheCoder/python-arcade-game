class Coder
    def initialize
      @rating = 0
    end
    
    def practice
      @rating += 1
    end
    
    def oh_one?
      @rating > 10  # Arbitrary threshold for O(1) rating
    end
  end
  
  def train_to_oh_one
    coder = Coder.new
    practice_count = 0
    
    until coder.oh_one?
      coder.practice
      practice_count += 1
    end
    
    puts "Reached O(1) after #{practice_count} practice sessions!"
  end
  
  # Run the training
  train_to_oh_one