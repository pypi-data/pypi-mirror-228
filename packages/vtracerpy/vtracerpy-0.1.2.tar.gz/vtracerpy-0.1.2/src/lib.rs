// Copyright 2020 Tsang Hao Fung. See the COPYRIGHT
// file at the top-level directory of this distribution and at
// http://rust-lang.org/COPYRIGHT.
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option. This file may not be copied, modified, or distributed
// except according to those terms.

mod config;
mod converter;
mod svg;

pub use config::*;
pub use converter::*;
pub use svg::*;

use pyo3::prelude::*;
use pyo3::exceptions::*;
use visioncortex::PathSimplifyMode;
use visioncortex::{Color, ColorImage, ColorName};
use numpy::{PyArray2, PyArray3};
use image::{DynamicImage, ImageBuffer, Luma, Rgb};
use visioncortex::color_clusters::{Runner, RunnerConfig, KeyingAction, HIERARCHICAL_MAX};

#[pyfunction]
fn binary_image_to_svg(
    _py: Python,
    image: &PyArray2<u8>,
    path_precision: u32,
    mode: String,
    corner_threshold: i32,
    length_threshold: f64,
    max_iterations: usize,
    splice_threshold: i32,
    filter_speckle: usize
) -> PyResult<String> {
    let arr = unsafe { image.as_array() };
    let (height, width) = arr.dim();
    let buffer = ImageBuffer::<Luma<u8>, _>::from_raw(width as u32, height as u32, arr.as_slice().unwrap().to_owned()).expect("Failed to convert to ImageBuffer");
    let img: DynamicImage = DynamicImage::ImageLuma8(buffer);
    let img = ColorImage { pixels: img.to_rgba8().as_raw().to_vec(), width, height };
    let img = img.to_binary_image(|x| x.r < 128);

    let clusters = img.to_clusters(false);

    // Convert mode from String to PathSimplifyMode here (Assuming your library uses such types)
    let mode = match mode.as_str() {
        "spline" => PathSimplifyMode::Spline,
        "polygon" => PathSimplifyMode::Polygon,
        "pixel" => PathSimplifyMode::None,
        // ... handle other modes here
        _ => return Err(PyErr::new::<PyValueError, _>("Invalid mode provided")),
    };

    let filter_speckle_area: usize = filter_speckle * filter_speckle;
    let mut svg = SvgFile::new(width, height, Some(path_precision));
    for i in 0..clusters.len() {
        let cluster = clusters.get_cluster(i);
        if cluster.size() >= filter_speckle_area {
            let paths = cluster.to_compound_path(
                mode,
                deg2rad(corner_threshold),
                length_threshold,
                max_iterations,
                deg2rad(splice_threshold),
            );
            svg.add_path(paths, Color::color(&ColorName::Black));
        }
    }
    Ok(format!("{}", svg))
}

#[pyfunction]
fn color_image_to_svg(
    _py: Python,
    image: &PyArray3<u8>,
    layer_difference: i32,
    filter_speckle: usize,
    color_precision: i32,
    hierarchical: String,
    path_precision: u32,
    mode: String,
    corner_threshold: i32,
    length_threshold: f64,
    max_iterations: usize,
    splice_threshold: i32,
) -> PyResult<String> {
    let arr = unsafe { image.as_array() };
    let (height, width, _channel) = arr.dim();
    let buffer = ImageBuffer::<Rgb<u8>, _>::from_raw(width as u32, height as u32, arr.as_slice().unwrap().to_owned()).expect("Failed to convert to ImageBuffer");
    let img: DynamicImage = DynamicImage::ImageRgb8(buffer);
    let mut img = ColorImage { pixels: img.to_rgba8().as_raw().to_vec(), width, height };

    let hierarchical = match hierarchical.as_str() {
        "stacked" => Hierarchical::Stacked,
        "cutout" => Hierarchical::Cutout,
        // ... handle other modes here
        _ => return Err(PyErr::new::<PyValueError, _>("Invalid mode provided")),
    };
    // Convert mode from String to PathSimplifyMode here (Assuming your library uses such types)
    let mode = match mode.as_str() {
        "spline" => PathSimplifyMode::Spline,
        "polygon" => PathSimplifyMode::Polygon,
        "pixel" => PathSimplifyMode::None,
        // ... handle other modes here
        _ => return Err(PyErr::new::<PyValueError, _>("Invalid mode provided")),
    };
    let key_color = if should_key_image(&img) {
        let key_color = find_unused_color_in_image(&img).map_err(|err| {
            PyErr::new::<PyValueError, _>(format!("Invalid image: {:?}", err))
        })?;
        for y in 0..height {
            for x in 0..width {
                if img.get_pixel(x, y).a == 0 {
                    img.set_pixel(x, y, &key_color);
                }
            }
        }
        key_color
    } else {
        // The default color is all zeroes, which is treated by visioncortex as a special value meaning no keying will be applied.
        Color::default()
    };

    let runner = Runner::new(RunnerConfig {
        diagonal: layer_difference == 0,
        hierarchical: HIERARCHICAL_MAX,
        batch_size: 25600,
        good_min_area: filter_speckle*filter_speckle,
        good_max_area: (width * height),
        is_same_color_a: 8 - color_precision,
        is_same_color_b: 1,
        deepen_diff: layer_difference,
        hollow_neighbours: 1,
        key_color,
        keying_action: if matches!(hierarchical, Hierarchical::Cutout) {
            KeyingAction::Keep
        } else {
            KeyingAction::Discard
        },
    }, img);

    let mut clusters = runner.run();

    match hierarchical {
        Hierarchical::Stacked => {}
        Hierarchical::Cutout => {
            let view = clusters.view();
            let image = view.to_color_image();
            let runner = Runner::new(RunnerConfig {
                diagonal: false,
                hierarchical: 64,
                batch_size: 25600,
                good_min_area: 0,
                good_max_area: (image.width * image.height) as usize,
                is_same_color_a: 0,
                is_same_color_b: 1,
                deepen_diff: 0,
                hollow_neighbours: 0,
                key_color,
                keying_action: KeyingAction::Discard,
            }, image);
            clusters = runner.run();
        },
    }

    let view = clusters.view();

    let mut svg = SvgFile::new(width, height, Some(path_precision));
    for &cluster_index in view.clusters_output.iter().rev() {
        let cluster = view.get_cluster(cluster_index);
        let paths = cluster.to_compound_path(
            &view,
            false,
            mode,
            deg2rad(corner_threshold),
            length_threshold,
            max_iterations,
            deg2rad(splice_threshold),
        );
        svg.add_path(paths, cluster.residue_color());
    }
    Ok(format!("{}", svg))
}


/// A Python module implemented in Rust.
#[pymodule]
fn vtracerpy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(binary_image_to_svg, m)?)?;
    m.add_function(wrap_pyfunction!(color_image_to_svg, m)?)?;
    Ok(())
}