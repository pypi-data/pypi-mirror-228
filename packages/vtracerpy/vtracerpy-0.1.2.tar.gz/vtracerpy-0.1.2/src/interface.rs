use pyo3::prelude::*;
use visioncortex::PathSimplifyMode;
use visioncortex::{Color, ColorImage, ColorName};
use super::svg::SvgFile;


/// Formats the sum of two numbers as string.
#[pyfunction]
fn image_to_svg(py: Python, image: &PyArray2<u8>) -> PyResult<String> {
    let mut image = image.as_array().to_owned();
    let (width, height) = (img.width() as usize, img.height() as usize);
    let img = ColorImage {pixels: img.as_raw().to_vec(), width, height};

    let img = img.to_binary_image(|x| x.r < 128);

    let clusters = img.to_clusters(false);

    let path_precision = Some(8);
    let mode = PathSimplifyMode::Spline;
    let corner_threshold = 60;
    let length_threshold = 4.0;
    let max_iterations = 10;
    let splice_threshold = 45;

    let mut svg = SvgFile::new(width, height, path_precision);
    for i in 0..clusters.len() {
        let cluster = clusters.get_cluster(i);
        if cluster.size() >= config.filter_speckle_area {
            let paths = cluster.to_compound_path(
                mode,
                corner_threshold,
                length_threshold,
                max_iterations,
                splice_threshold,
            );
            svg.add_path(paths, Color::color(&ColorName::Black));
        }

    Ok(svg)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn pyvtracer(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(image_to_svg, m)?)?;
    Ok(())
}