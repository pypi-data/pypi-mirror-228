extern crate rand;

use pyo3::prelude::*;
use rand::seq::SliceRandom;
use std::collections::HashSet;

#[pyfunction]
fn wright_fisher_sim(stem_cell_size: usize, generation_time: u64) -> (Vec<Vec<i64>>, Vec<u64>) {
    let max_generations = 10000;
    let ancestors: Vec<i64> = (0..stem_cell_size as i64).collect();

    let mut pop = Vec::with_capacity(max_generations);
    pop.push(ancestors.clone());

    let mut rng = rand::thread_rng();

    let mut unique_cells: HashSet<i64> = HashSet::with_capacity(stem_cell_size);
    let mut current_gen = 1;
    while current_gen < max_generations {
        let sample: Vec<i64> = (0..stem_cell_size)
            .map(|_| *pop[current_gen - 1].choose(&mut rng).unwrap())
            .collect();

        unique_cells.extend(&sample);
        if unique_cells.len() == 1 {
            break;
        }

        pop.push(sample);
        current_gen += 1;
        unique_cells.clear();
    }

    let time_vector: Vec<u64> = (0..current_gen).map(|x| x as u64 * generation_time).collect();
    (pop, time_vector)
}


fn auc(x: &[u64], y: &[usize]) -> f64 {
    let direction = if x[0] < x[1] {
        1.0
    } else if x[0] > x[1] {
        -1.0
    } else {
        panic!("x must not be constant");
    };

    x.windows(2).zip(y.windows(2))
        .map(|(xw, yw)| {
            direction * (xw[1] - xw[0]) as f64 * (yw[0] + yw[1]) as f64 / 2.0
        })
        .sum()
}

#[pyfunction]
fn ltt_auc(stem_cell_size: usize, generation_time: u64) -> f64 {
    let (pop, time_vector) = wright_fisher_sim(stem_cell_size, generation_time);
    let lineages: Vec<usize> = pop.iter()
        .map(|x| {
            let mut unique_cells: HashSet<i64> = HashSet::with_capacity(stem_cell_size);
            unique_cells.extend(x.iter());
            unique_cells.len()
        })
        .collect();
    auc(&time_vector, &lineages)
}


#[pyfunction]
fn fused_ltt_auc(stem_cell_size: usize, generation_time: u64) -> f64{
    let max_generations = 10000;
    let ancestors: Vec<i64> = (0..stem_cell_size as i64).collect();

    let mut pop = ancestors.clone();

    let mut rng = rand::thread_rng();

    let mut unique_cells: HashSet<i64> = HashSet::with_capacity(stem_cell_size);
    let mut lineages = Vec::with_capacity(max_generations);
    let mut time_vector = Vec::with_capacity(max_generations);
    
    let mut current_gen = 0;
    while current_gen < max_generations {
        unique_cells.extend(&pop);
        lineages.push(unique_cells.len());
        time_vector.push(current_gen as u64 * generation_time);
        
        if unique_cells.len() == 1 {
            break;
        }

        pop = (0..stem_cell_size)
            .map(|_| *pop.choose(&mut rng).unwrap())
            .collect();

        current_gen += 1;
        unique_cells.clear();
    }

    auc(&time_vector, &lineages)
}




/// A Python module implemented in Rust.
#[pymodule]
fn wfrs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(wright_fisher_sim, m)?)?;
    m.add_function(wrap_pyfunction!(ltt_auc, m)?)?;
    m.add_function(wrap_pyfunction!(fused_ltt_auc, m)?)?;
    Ok(())
}