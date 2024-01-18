use cpython::{PyResult, Python, py_module_initializer, py_fn};

py_module_initializer!(RSmiscLib, |py, m| {
    m.add(py, "__doc__", "This module is implemented in Rust.")?;
    m.add(py, "str_replacer", py_fn!(py, str_replacer(initial_string: String, ch: String, replacing_character: String, occurrence: i64)))?;
    Ok(())
});

pub fn str_replacer(_py: Python, initial_string: String, ch: String, replacing_character: String, occurrence: i64) -> PyResult<String> {
    let mut result: String = "".to_string();
    let mut count = 0;
    for c in initial_string.chars() {
        if c == ch.chars().nth(0).unwrap() {
            count += 1;
            if count == occurrence {
                result.push(replacing_character.chars().nth(0).unwrap());
                count = 0;
            } else {
                result.push(c);
            }
        } else {
            result.push(c);
        }
    }
    
    Ok(result)
}
