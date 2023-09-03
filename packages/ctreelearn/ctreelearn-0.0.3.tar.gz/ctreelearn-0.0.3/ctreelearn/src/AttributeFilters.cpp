
#include "../include/AttributeFilters.hpp"


    AttributeFilters::AttributeFilters(ComponentTree* tree){
        this->tree = tree;
    }

    py::array_t<int> AttributeFilters::filteringByPruningMin(py::array_t<double> &attr, double threshold){

        auto bufAttribute = attr.request();
        
        double *attribute = (double *) bufAttribute.ptr;

        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        auto imgNumpy = py::array(py::buffer_info(
                nullptr,            
                sizeof(int),     
                py::format_descriptor<int>::value, 
                1,         
                { ( n ) }, 
                { sizeof(int) }
            ));
        auto bufImgOutput = imgNumpy.request();
        int *imgOutput = (int *) bufImgOutput.ptr;

        AttributeFilters::filteringByPruningMin(this->tree, attribute, threshold, imgOutput);

        return imgNumpy;
    }

    py::array_t<int> AttributeFilters::filteringByPruningMax(py::array_t<double> &attr, double threshold){

        auto bufAttribute = attr.request();
        
        double *attribute = (double *) bufAttribute.ptr;

        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        auto imgNumpy = py::array(py::buffer_info(
                nullptr,            
                sizeof(int),     
                py::format_descriptor<int>::value, 
                1,         
                { ( n ) }, 
                { sizeof(int) }
            ));
        auto bufImgOutput = imgNumpy.request();
        int *imgOutput = (int *) bufImgOutput.ptr;

        AttributeFilters::filteringByPruningMax(this->tree, attribute, threshold, imgOutput);

        return imgNumpy;

    }

    py::array_t<int> AttributeFilters::filteringByPruningMin(std::vector<bool> criterion){

        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        auto imgNumpy = py::array(py::buffer_info(
                nullptr,            
                sizeof(int),     
                py::format_descriptor<int>::value, 
                1,         
                { ( n ) }, 
                { sizeof(int) }
            ));
        auto bufImgOutput = imgNumpy.request();
        int *imgOutput = (int *) bufImgOutput.ptr;

        AttributeFilters::filteringByPruningMin(this->tree, criterion, imgOutput);

        return imgNumpy;
    }

    py::array_t<int> AttributeFilters::filteringByDirectRule(std::vector<bool> criterion){

        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        auto imgNumpy = py::array(py::buffer_info(
                nullptr,            
                sizeof(int),     
                py::format_descriptor<int>::value, 
                1,         
                { ( n ) }, 
                { sizeof(int) }
            ));
        auto bufImgOutput = imgNumpy.request();
        int *imgOutput = (int *) bufImgOutput.ptr;

        AttributeFilters::filteringByDirectRule(this->tree, criterion, imgOutput);

        return imgNumpy;
    }

    py::array_t<int> AttributeFilters::filteringByPruningMax(std::vector<bool> criterion){

        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        auto imgNumpy = py::array(py::buffer_info(
                nullptr,            
                sizeof(int),     
                py::format_descriptor<int>::value, 
                1,         
                { ( n ) }, 
                { sizeof(int) }
            ));
        auto bufImgOutput = imgNumpy.request();
        int *imgOutput = (int *) bufImgOutput.ptr;

        AttributeFilters::filteringByPruningMax(this->tree, criterion, imgOutput);

        return imgNumpy;

    }

    py::array_t<int> AttributeFilters::filteringBySubtractiveRule(std::vector<bool> criterion){

        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        auto imgNumpy = py::array(py::buffer_info(
                nullptr,            
                sizeof(int),     
                py::format_descriptor<int>::value, 
                1,         
                { ( n ) }, 
                { sizeof(int) }
            ));
        auto bufImgOutput = imgNumpy.request();
        int *imgOutput = (int *) bufImgOutput.ptr;

        AttributeFilters::filteringBySubtractiveRule(this->tree, criterion, imgOutput);

        return imgNumpy;

    }

    py::array_t<double> AttributeFilters::filteringBySubtractiveScoreRule(std::vector<double> prob){

        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        auto imgNumpy = py::array(py::buffer_info(
                nullptr,            
                sizeof(double),     
                py::format_descriptor<double>::value, 
                1,         
                { ( n ) }, 
                { sizeof(double) }
            ));
        auto bufImgOutput = imgNumpy.request();
        double *imgOutput = (double *) bufImgOutput.ptr;

        AttributeFilters::filteringBySubtractiveScoreRule(this->tree, prob, imgOutput);

        return imgNumpy;

    }
