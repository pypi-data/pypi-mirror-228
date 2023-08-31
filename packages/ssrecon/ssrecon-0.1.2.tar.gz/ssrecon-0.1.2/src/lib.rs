use itertools::Itertools;
use pyo3::prelude::*;

#[pyfunction]
fn find_match(
    nums: Vec<(f64, usize)>,
    target: f64,
    combos: usize,
    debug: bool
) -> PyResult<(Option<Vec<usize>>, Option<Vec<f64>>)> {
    for len in 1..=combos {
        if debug {println!("Attempting with {:?} combos", len);}
        for combination in nums.iter().combinations(len) {
            let (values, keys): (Vec<f64>, Vec<usize>) = combination.into_iter().cloned().unzip();
            if (values.iter().sum::<f64>() - target).abs() < 1e-6 {
                return Ok((Some(keys), Some(values)));
            }
        }
    }

    Ok((None,None))
}

/// A Python module implemented in Rust.
#[pymodule]
fn ssrecon(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find_match, m)?)?;
    Ok(())
}
