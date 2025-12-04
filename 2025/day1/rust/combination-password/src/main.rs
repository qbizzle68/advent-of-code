use std::fs::File;
use std::io::{self, BufRead, BufReader};


fn import_data() ->  Result<Vec<i32>, Box<dyn std::error::Error>>{
    let file_path = "../../input.txt"; // Must be ran from the create root
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);


/*    let mut values: Vec<i32> = Vec::new();
    for line in reader.lines() {
        let line = line?;
        let num: i32 = line[1..].parse::<i32>().expect("Failed to parse string to i32");
        println!("Parsed number: {}", num);
    }
    
    values*/

    let values: Vec<i32> = Vec::new();
    Ok(values)
}


fn main() {
    let values = import_data();
}
