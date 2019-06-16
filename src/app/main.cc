#include <gtkmm.h>
#include <iostream>
#include <fstream>
#include <string>

#include "parser.h"


class MainWindow {
  public:
    MainWindow();
    void run(int argc, char **argv);

  protected:
    Glib::RefPtr<Gtk::Application> app;
    Glib::RefPtr<Gtk::Builder> builder;
    Glib::RefPtr<Gtk::TextBuffer> buffer;
    Glib::RefPtr<Gtk::Clipboard> clipboard;

    Gtk::ApplicationWindow* window = nullptr;
    Gtk::AboutDialog* aboutDialog = nullptr;
    Gtk::TextView* textView = nullptr;

    Parser* parser;

    void apply();
    void openFile();
    void saveFile();
    void about();
    void copyAll() { clipboard->set_text(buffer->get_text()); };
    void clear() { buffer->set_text(""); };
    void paste() { buffer->paste_clipboard(clipboard); };
    void exit() { window->close(); };

    void loadData();
};


MainWindow::MainWindow() {
  app = Gtk::Application::create("com.bretahajek.diakritik");
  clipboard = Gtk::Clipboard::get();

  builder = Gtk::Builder::create();
  try {
    builder->add_from_file("main.glade");
  } catch(const Glib::FileError& ex) {
    std::cerr << "FileError: " << ex.what() << std::endl;
  } catch(const Glib::MarkupError& ex) {
    std::cerr << "MarkupError: " << ex.what() << std::endl;
  } catch(const Gtk::BuilderError& ex) {
    std::cerr << "BuilderError: " << ex.what() << std::endl;
  }

  // Widgets
  builder->get_widget("about_dialog", aboutDialog);
  builder->get_widget("window", window);
  builder->get_widget("text_view", textView);
  buffer = textView->get_buffer();

  // Menu
  Gtk::ImageMenuItem* mBtn;
  builder->get_widget("exit_button", mBtn);
  mBtn->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::exit));
  builder->get_widget("about_button", mBtn);
  mBtn->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::about));
  builder->get_widget("paste_button", mBtn);
  mBtn->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::paste));
  builder->get_widget("clear_button", mBtn);
  mBtn->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::clear));
  builder->get_widget("copy_button1", mBtn);
  mBtn->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::copyAll));
  builder->get_widget("save_button1", mBtn);
  mBtn->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::saveFile));
  builder->get_widget("open_button1", mBtn);
  mBtn->signal_activate().connect(
    sigc::mem_fun(*this, &MainWindow::openFile));

  Gtk::Button* btn;
  builder->get_widget("copy_button2", btn);
  btn->signal_clicked().connect(
    sigc::mem_fun(*this, &MainWindow::copyAll));
  builder->get_widget("save_button2", btn);
  btn->signal_clicked().connect(
    sigc::mem_fun(*this, &MainWindow::saveFile));
  builder->get_widget("open_button2", btn);
  btn->signal_clicked().connect(
    sigc::mem_fun(*this, &MainWindow::openFile));
  builder->get_widget("apply_button", btn);
  btn->signal_clicked().connect(
    sigc::mem_fun(*this, &MainWindow::apply));
}


void MainWindow::run(int argc, char** argv) {
  if (Glib::thread_supported()) {
    Glib::thread_init();
    Glib::Thread::create(sigc::mem_fun(*this, &MainWindow::loadData), true);
  } else {
    std::cout << "Vlákna nejsou podporovaná!" << std::endl;
    std::cout << "Aplikace se bude načítat déle." << std::endl;
    loadData();
  }
  app->run(*window, argc, argv);
}


void MainWindow::loadData() {
  auto start = std::chrono::steady_clock::now();
  std::cout << "Loading data: " << std::flush;
  parser = new Parser("../obj/dictionary.dic");

  // Aktivace tlačítka "apply"
  std::cout << "finished!" << std::endl;
  Gtk::Button* btn;
  builder->get_widget("apply_button", btn);
  btn->set_sensitive(true);
  Gtk::Widget* widget;
  builder->get_widget("apply_button_spinner", widget);
  widget->set_visible(false);
  builder->get_widget("apply_button_icon", widget);
  widget->set_visible(true);

  auto end = std::chrono::steady_clock::now();

  std::cout << "Doba načítání: "
            << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
            << " ms" << std::endl;
}


void MainWindow::apply() {
  std::string text = buffer->get_text();
  parser->processText(text);
  buffer->set_text(text);
}


void MainWindow::about() {
  if (aboutDialog) {
    aboutDialog->run();
    aboutDialog->close();
  }
}


void MainWindow::saveFile() {
  Gtk::FileChooserDialog dialog("File Select", Gtk::FILE_CHOOSER_ACTION_SAVE);
  dialog.set_transient_for(*window);
  dialog.add_button(Gtk::Stock::CANCEL, Gtk::RESPONSE_CANCEL);
  dialog.add_button(Gtk::Stock::SAVE, Gtk::RESPONSE_OK);

  int res = dialog.run();
  switch(res) {
  case(Gtk::RESPONSE_OK): {
    std::ofstream fs;
    std::string text = buffer->get_text();

    fs.open(dialog.get_filename().c_str());
    fs.write(text.c_str(), text.size());
    fs.close();
    break;
  }
  case(Gtk::RESPONSE_CANCEL):
    break;
  default:
    break;
  }
}


void MainWindow::openFile() {
  Gtk::FileChooserDialog dialog("File Select", Gtk::FILE_CHOOSER_ACTION_OPEN);
  dialog.set_transient_for(*window);
  dialog.add_button(Gtk::Stock::CANCEL, Gtk::RESPONSE_CANCEL);
  dialog.add_button(Gtk::Stock::OPEN, Gtk::RESPONSE_OK);

  int res = dialog.run();
  switch(res) {
  case(Gtk::RESPONSE_OK): {
    clear();    // Smazani puvodniho obsahu
    std::ifstream fs;
    std::string line;
    auto position = buffer->begin();

    fs.open(dialog.get_filename().c_str());
    if (fs) {
      while (std::getline(fs, line)) {
        position = buffer->insert(position, line + "\n");
      }
      fs.close();
    }
    break;
  }
  case(Gtk::RESPONSE_CANCEL):
    break;
  default:
    break;
  }
}


int main (int argc, char **argv) {
  MainWindow window;
  window.run(argc, argv);

  return 0;
}
